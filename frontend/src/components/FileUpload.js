import {useForm} from 'react-hook-form';

import api from '../api';


export default function FileUpload() {
    const {register, handleSubmit} = useForm();

    const onSubmit = (data) => {
        const formData = new FormData();
        formData.append("file", data.upfile[0]);

        api.post('/push', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            }
        }).then((response) => {
            console.log(response);
        }).catch((error) => {
            console.log(error);
        });
        console.log(data);
    }

    return (
        <>
            <h2>Upload files</h2>
            <form onSubmit={handleSubmit(onSubmit)}>
                <input
                    {...register("upfile", {required: "Required"})}
                    type="file"
                    name="upfile"/>
                <button>Submit</button>
            </form>
        </>
    );
}
