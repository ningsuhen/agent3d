"use strict";
// User model TypeScript file
// Referenced in test-navigation.md
Object.defineProperty(exports, "__esModule", { value: true });
exports.UserModel = void 0;
// TC-002: File reference detection test
// REQ-002: Handle multiple file references
class UserModel {
    constructor(user) {
        this.user = user;
    }
    getName() {
        return this.user.name;
    }
}
exports.UserModel = UserModel;
//# sourceMappingURL=user.js.map