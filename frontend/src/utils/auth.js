// Lightweight helpers around what's already stored at login.
// No extra dependency needed — a JWT's payload is just base64.

export function getRole() {

    return localStorage.getItem("role");

}

export function isAdmin() {

    return getRole() === "admin";

}

export function getCurrentUserId() {

    const token = localStorage.getItem("token");

    if (!token) return null;

    try {

        const payload = token.split(".")[1];

        const decoded = JSON.parse(atob(payload.replace(/-/g, "+").replace(/_/g, "/")));

        // flask-jwt-extended stores the identity in "sub"
        return decoded.sub;

    } catch (err) {

        return null;

    }

}
