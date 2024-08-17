import { useState } from 'react';
import {useNavigate} from "react-router-dom";

import api from '../api';
import {useAuth} from "../AuthContext";


export default function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [signedIn, setSignedIn] = useState(false);

    const navigate = useNavigate();

    const { setAuth } = useAuth();

    const validateForm = () => {
        if (!username || !password) {
            setError('Username and password are required');
            return false;
        }
        setError('');
        return true;
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!validateForm()) return;
        setLoading(true);

        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        api.post('/token', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',

            }
        }).then((response) => {
            localStorage.setItem('token', response.data.access_token);
            setAuth(true);
            navigate('/files');
        }).catch((error) => {
            setLoading(false);
            setSignedIn(true);
            setError('An error occurred. Try again later.');
        })

        setLoading(false);
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username: </label>
                    <input type="text"
                           value={username}
                           onChange={(e) => setUsername(e.target.value)}
                           />
                </div>
                <div>
                    <label>Password: </label>
                    <input type="password"
                           value={password}
                           onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button type="submit" disabled={loading}>
                    {loading ? 'Logging in...' : 'Login'}
                </button>
                {error && <p style={{ color: 'red' }}>{error}</p>}
            </form>
        </div>
    )

}