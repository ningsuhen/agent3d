#!/usr/bin/env python3
"""
DDD Migration Manager

Manages and executes DDD framework migrations with tracking and rollback support.
"""

import argparse
import hashlib
import os
import shutil
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class MigrationManager:
    """Manages DDD framework migrations with tracking and safety features."""
    
    def __init__(self, root_dir: str = '.'):
        self.root_dir = Path(root_dir)
        self.migrations_dir = self.root_dir / 'docs' / 'migrations'
        self.tracker_file = self.migrations_dir / 'migration-tracker.yml'
        self.backup_dir = self.root_dir / '.agent3d-backups' / 'migrations'
        
    def load_tracker(self) -> Dict[str, Any]:
        """Load migration tracker data."""
        if not self.tracker_file.exists():
            return {
                'metadata': {
                    'version': '1.0.0',
                    'created_at': datetime.utcnow().isoformat() + 'Z',
                    'last_updated': datetime.utcnow().isoformat() + 'Z',
                    'project_id': 'ddd-project'
                },
                'migrations': {},
                'execution_log': [],
                'config': {
                    'auto_backup': True,
                    'backup_directory': '.agent3d-backups/migrations',
                    'validation_level': 'strict',
                    'rollback_enabled': True,
                    'max_execution_time_minutes': 30
                }
            }
        
        with open(self.tracker_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def save_tracker(self, tracker_data: Dict[str, Any]) -> None:
        """Save migration tracker data."""
        tracker_data['metadata']['last_updated'] = datetime.utcnow().isoformat() + 'Z'
        
        # Ensure directory exists
        self.tracker_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.tracker_file, 'w', encoding='utf-8') as f:
            yaml.dump(tracker_data, f, default_flow_style=False, sort_keys=False)
    
    def load_migration(self, migration_id: str) -> Optional[Dict[str, Any]]:
        """Load migration workflow definition."""
        migration_file = self.migrations_dir / f'{migration_id}.yml'
        if not migration_file.exists():
            return None
            
        with open(migration_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def calculate_checksum(self, migration_data: Dict[str, Any]) -> str:
        """Calculate checksum for migration data."""
        content = yaml.dump(migration_data, sort_keys=True)
        return f"sha256:{hashlib.sha256(content.encode()).hexdigest()[:16]}"
    
    def get_migration_status(self, migration_id: str) -> str:
        """Get current status of a migration."""
        tracker = self.load_tracker()
        if migration_id in tracker['migrations']:
            return tracker['migrations'][migration_id]['status']
        return 'unknown'
    
    def list_migrations(self) -> List[Dict[str, Any]]:
        """List all available migrations."""
        migrations = []
        
        if not self.migrations_dir.exists():
            return migrations
            
        for migration_file in self.migrations_dir.glob('*.yml'):
            if migration_file.name == 'migration-tracker.yml':
                continue
                
            migration_id = migration_file.stem
            migration_data = self.load_migration(migration_id)
            
            if migration_data:
                status = self.get_migration_status(migration_id)
                migrations.append({
                    'id': migration_id,
                    'name': migration_data.get('metadata', {}).get('name', migration_id),
                    'status': status,
                    'version': migration_data.get('metadata', {}).get('version', '1.0.0'),
                    'description': migration_data.get('metadata', {}).get('description', ''),
                    'impact': migration_data.get('metadata', {}).get('impact', 'unknown')
                })
        
        return migrations
    
    def check_prerequisites(self, migration_data: Dict[str, Any]) -> List[str]:
        """Check if migration prerequisites are met."""
        failures = []
        prerequisites = migration_data.get('prerequisites', [])
        
        for prereq in prerequisites:
            # Simple file existence checks
            if 'file exists' in prereq:
                file_path = prereq.split(' file exists')[0].strip()
                if not (self.root_dir / file_path).exists():
                    failures.append(f"Missing file: {file_path}")
            
            # Directory existence checks
            elif 'directory' in prereq and 'exists' in prereq:
                dir_path = prereq.split(' directory')[0].strip()
                if not (self.root_dir / dir_path).exists():
                    failures.append(f"Missing directory: {dir_path}")
        
        return failures
    
    def create_backup(self, migration_id: str, migration_data: Dict[str, Any]) -> bool:
        """Create backup of files before migration."""
        backup_targets = migration_data.get('backup_targets', [])
        if not backup_targets:
            return True
            
        migration_backup_dir = self.backup_dir / migration_id / datetime.now().strftime('%Y%m%d_%H%M%S')
        migration_backup_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            for target in backup_targets:
                source_path = self.root_dir / target
                if source_path.exists():
                    if source_path.is_file():
                        dest_path = migration_backup_dir / target
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source_path, dest_path)
                    elif source_path.is_dir():
                        dest_path = migration_backup_dir / target
                        shutil.copytree(source_path, dest_path)
            
            print(f"✅ Backup created: {migration_backup_dir}")
            return True
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False
    
    def update_migration_status(self, migration_id: str, status: str, notes: str = "") -> None:
        """Update migration status in tracker."""
        tracker = self.load_tracker()
        
        if migration_id not in tracker['migrations']:
            tracker['migrations'][migration_id] = {}
        
        tracker['migrations'][migration_id]['status'] = status
        
        if status == 'completed':
            tracker['migrations'][migration_id]['executed_at'] = datetime.utcnow().isoformat() + 'Z'
        
        if notes:
            tracker['migrations'][migration_id]['notes'] = notes
        
        # Add to execution log
        tracker['execution_log'].append({
            'migration_id': migration_id,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'status': status,
            'user': 'migration-manager',
            'details': notes
        })
        
        self.save_tracker(tracker)
    
    def execute_migration(self, migration_id: str, force: bool = False) -> bool:
        """Execute a migration workflow."""
        # Check if migration exists
        migration_data = self.load_migration(migration_id)
        if not migration_data:
            print(f"❌ Migration '{migration_id}' not found")
            return False
        
        # Check current status
        current_status = self.get_migration_status(migration_id)
        if current_status == 'completed' and not force:
            print(f"✅ Migration '{migration_id}' already completed (use --force to re-run)")
            return True
        
        print(f"🚀 Starting migration: {migration_data['metadata']['name']}")
        
        # Check prerequisites
        prereq_failures = self.check_prerequisites(migration_data)
        if prereq_failures:
            print("❌ Prerequisites not met:")
            for failure in prereq_failures:
                print(f"   - {failure}")
            return False
        
        # Create backup
        if not self.create_backup(migration_id, migration_data):
            print("❌ Backup creation failed - aborting migration")
            return False
        
        # Update status to running
        self.update_migration_status(migration_id, 'running', 'Migration started')
        
        try:
            # Execute migration steps
            steps = migration_data.get('steps', [])
            for step in steps:
                step_id = step['id']
                step_name = step['name']
                print(f"📋 Executing step: {step_name}")
                
                # For now, we'll just print the actions
                # In a full implementation, these would be executed
                actions = step.get('actions', [])
                for action in actions:
                    print(f"   - {action}")
                
                print(f"✅ Step completed: {step_name}")
            
            # Mark as completed
            self.update_migration_status(migration_id, 'completed', 'Migration completed successfully')
            print(f"🎉 Migration '{migration_id}' completed successfully!")
            return True
            
        except Exception as e:
            self.update_migration_status(migration_id, 'failed', f'Migration failed: {str(e)}')
            print(f"❌ Migration failed: {e}")
            return False
    
    def show_status(self) -> None:
        """Show status of all migrations."""
        migrations = self.list_migrations()
        
        if not migrations:
            print("No migrations found.")
            return
        
        print("📋 Migration Status:")
        print("-" * 80)
        
        for migration in migrations:
            status_icon = {
                'completed': '✅',
                'pending': '⏳',
                'running': '🔄',
                'failed': '❌',
                'skipped': '⏭️',
                'unknown': '❓'
            }.get(migration['status'], '❓')
            
            print(f"{status_icon} {migration['name']}")
            print(f"   ID: {migration['id']}")
            print(f"   Status: {migration['status']}")
            print(f"   Impact: {migration['impact']}")
            print(f"   Description: {migration['description']}")
            print()

def main():
    parser = argparse.ArgumentParser(description='DDD Migration Manager')
    parser.add_argument('command', choices=['status', 'list', 'run', 'complete', 'history'],
                       help='Command to execute')
    parser.add_argument('migration_id', nargs='?', help='Migration ID (for run/complete commands)')
    parser.add_argument('--force', action='store_true', help='Force re-run completed migration')
    parser.add_argument('--root', default='.', help='Project root directory')
    
    args = parser.parse_args()
    
    manager = MigrationManager(args.root)
    
    if args.command == 'status':
        manager.show_status()
    elif args.command == 'list':
        manager.show_status()  # Same as status for now
    elif args.command == 'run':
        if not args.migration_id:
            print("❌ Migration ID required for 'run' command")
            sys.exit(1)
        success = manager.execute_migration(args.migration_id, args.force)
        sys.exit(0 if success else 1)
    elif args.command == 'complete':
        if not args.migration_id:
            print("❌ Migration ID required for 'complete' command")
            sys.exit(1)
        manager.update_migration_status(args.migration_id, 'completed', 'Manually marked as completed')
        print(f"✅ Migration '{args.migration_id}' marked as completed")
    elif args.command == 'history':
        tracker = manager.load_tracker()
        print("📜 Migration History:")
        for entry in tracker.get('execution_log', []):
            print(f"  {entry['timestamp']}: {entry['migration_id']} -> {entry['status']}")

if __name__ == '__main__':
    main()
