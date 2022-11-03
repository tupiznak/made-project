export class LocalStorage {
    setIsAuthenticated(isAuth) {
        if (process.client) {
            localStorage.setItem('isAuthenticated', isAuth)
        }
    }

    setUser(user) {
        if (process.client) {
            localStorage.setItem('user', JSON.stringify(user))
        }
    }

    getIsAuthenticated() {
        if (process.client) {
            return localStorage.getItem('isAuthenticated')
        }
    }

    getUser() {
        if (process.client) {
            return JSON.parse(localStorage.getItem('user'))
        }
    }

    removeIsAuthenticated() {
        if (process.client) {
            localStorage.removeItem('isAuthenticated')
        }
    }

    removeUser() {
        if (process.client) {
            localStorage.removeItem('user')
        }
    }

    raiseLocalstorageChangedEvent() {
        if (process.client) {
            window.dispatchEvent(new CustomEvent('user-localstorage-changed', {
                detail: {
                    isAuth: localStorage.getItem('isAuthenticated'),
                    user: localStorage.getItem('user')
                }
            }));
        }
    }

    pushToLoginIfNotAuthenticated() {
        if (process.client) {
            const router = useRouter();
            if (!localStorage.getItem('isAuthenticated')) {
                router.push({ path: "/login" });
            }
        }
    }
}