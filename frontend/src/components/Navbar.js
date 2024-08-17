import {Link, useMatch, useResolvedPath} from "react-router-dom";
import {useAuth} from "../AuthContext";

export default function Navbar() {
    const {auth} = useAuth();

    return (
        <nav className="nav">
            <Link to="/" className="site-title">
                Upload Service
            </Link>
            <ul>
                {auth ?
                    <>
                        <CustomLink to="/files">File list</CustomLink>
                        <CustomLink to="/upload">Upload</CustomLink>
                        <CustomLink to="/logout">Log Out</CustomLink>
                    </>
                    : <CustomLink to="/login">Log In</CustomLink>
                }
            </ul>
        </nav>
    )
}

function CustomLink({to, children, ...props}) {
    const resolvedPath = useResolvedPath(to);
    const isActive = useMatch({path: resolvedPath.pathname, end: true});

    return (
        <li className={isActive ? "active" : ""}>
            <Link to={to} {...props}>
                {children}
            </Link>
        </li>
    )
}