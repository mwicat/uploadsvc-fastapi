import {BrowserRouter, Route, Routes} from 'react-router-dom';

import FileList from './components/FileList';
import FileUpload from './components/FileUpload';

// import logo from './logo.svg';

import './App.css';
import Navbar from "./components/Navbar";
import Home from "./components/Home";


function App() {
    return (
        <>
            <BrowserRouter>
                <Navbar/>
                <div className="container">
                    <Routes>
                        <Route path="/" element={<Home/>}/>
                        <Route path="/files" element={<FileList/>}/>
                        <Route path="/upload" element={<FileUpload/>}/>
                    </Routes>
                </div>
            </BrowserRouter>
        </>
    );
}

export default App;
