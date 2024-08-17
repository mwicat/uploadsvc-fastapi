import { createContext, useContext, useEffect, useState } from 'react';
import api from "./api";

const AuthContext = createContext({
  auth: null,
  setAuth: () => {},
  user: null,
});

export const useAuth = () => useContext(AuthContext);

const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState(null);
  const [user, setUser] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem('token');
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        setAuth(token !== null);
    }, []);

  return (
    <AuthContext.Provider value={{ auth, setAuth, user }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;