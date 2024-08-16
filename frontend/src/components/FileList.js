import {useEffect, useState} from 'react';

import api from '../api';


export default function FileList() {
    const [files, setFiles] = useState([]);

    const getFileList = async () => {
        const response = await api.get('/files');
        setFiles(response.data.file_list);
    };

    useEffect(() => {
        getFileList();
    }, []);

    const fileLst = files.map(file => {
            const url = `/files/${file}`;
            const params = {};
            return (
                <li key={file}><a href={api.getUri({url, params})}>{file}</a></li>
            )
        }
    );

    return (
        <>
            <h2>Files</h2>
            {fileLst.length > 0 ? <ul>{fileLst}</ul> : <p>File list is empty</p>}
        </>
    );
}
