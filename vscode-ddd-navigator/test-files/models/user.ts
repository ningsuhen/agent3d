// User model TypeScript file
// Referenced in test-navigation.md

export interface User {
    id: number;
    name: string;
    email: string;
}

// TC-002: File reference detection test
// REQ-002: Handle multiple file references

export class UserModel {
    constructor(private user: User) {}
    
    getName(): string {
        return this.user.name;
    }
}
