// Sample JavaScript file with test case references
// This file demonstrates that the extension works in code files, not just markdown

/**
 * User authentication module
 * Implements REQ-001 and REQ-AUTH-001
 * Tested by TC-0001, TC-0002, TC-0003a
 */
class UserAuth {
    constructor() {
        // TC-ENV-001: Environment configuration
        this.config = process.env;
    }

    /**
     * Login method
     * Covers TC-0001 (valid credentials) and TC-0002 (invalid credentials)
     */
    async login(username, password) {
        // Implementation for REQ-001
        if (!username || !password) {
            // This scenario is covered by TC-0002
            throw new Error('Invalid credentials');
        }

        // TC-ENV-002: Environment-based configuration
        const authService = this.getAuthService();
        
        try {
            // TC-SYNC-001: Data synchronization
            const result = await authService.authenticate(username, password);
            return result;
        } catch (error) {
            // TC-0003a: Handle expired sessions
            if (error.code === 'SESSION_EXPIRED') {
                throw new Error('Session expired');
            }
            throw error;
        }
    }

    /**
     * Batch processing method
     * Implements REQ-BATCH-001
     * Tested by TC-BATCH-001 and TC-BATCH-002
     */
    async processBatch(requests) {
        // TC-BATCH-001: Parallel execution strategy
        const promises = requests.map(req => this.processRequest(req));
        
        try {
            // TC-ENV-007: Environment validation
            const results = await Promise.all(promises);
            return results;
        } catch (error) {
            // TC-SYNC-002: Conflict resolution
            console.error('Batch processing failed:', error);
            throw error;
        }
    }
}

// Export for testing
// Tests should validate TC-0001, TC-0002, TC-0003a, TC-ENV-001, TC-ENV-002, TC-ENV-007
// Also covers TC-BATCH-001, TC-BATCH-002, TC-SYNC-001, TC-SYNC-002
module.exports = UserAuth;
