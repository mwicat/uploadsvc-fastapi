import {useAuth} from "../AuthContext";


export default function Logout() {
    const { setAuth } = useAuth();
    localStorage.clear();
    setAuth(false);

    return (
        <div>
            You have been logged out.
        </div>
    )
}