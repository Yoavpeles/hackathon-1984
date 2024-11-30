import React, { useState } from 'react';

const SteganographyTool = () => {
    const [image, setImage] = useState<File | null>(null);
    const [message, setMessage] = useState('');
    const [outputPath, setOutputPath] = useState('');
    const [decodedMessage, setDecodedMessage] = useState('');

    const handleEncode = async () => {
        if (!image || !message) return alert('Please provide an image and a message.');

        const formData = new FormData();
        formData.append('image', image);
        formData.append('message', message);
        formData.append('output_path', 'encoded_image.png');

        try {
            const response = await fetch('http://127.0.0.1:5000/encode', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();
            if (data.status === 'success') {
                alert(`Message encoded successfully! Saved as: ${data.output_path}`);
            } else {
                alert(`Error: ${data.message}`);
            }
        } catch (error) {
            console.error(error);
            alert('Failed to encode message.');
        }
    };

    const handleDecode = async () => {
        if (!image) return alert('Please provide an image.');

        const formData = new FormData();
        formData.append('image', image);

        try {
            const response = await fetch('http://127.0.0.1:5000/decode', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();
            if (data.status === 'success') {
                setDecodedMessage(data.message);
            } else {
                alert(`Error: ${data.message}`);
            }
        } catch (error) {
            console.error(error);
            alert('Failed to decode message.');
        }
    };

    return (
        <div>
            <h1>Steganography Tool</h1>
            <div>
                <label>
                    Select Image:
                    <input type="file" onChange={(e) => setImage(e.target.files?.[0] || null)} />
                </label>
            </div>
            <div>
                <label>
                    Message to Encode:
                    <input type="text" value={message} onChange={(e) => setMessage(e.target.value)} />
                </label>
            </div>
            <div>
                <button onClick={handleEncode}>Encode Message</button>
                <button onClick={handleDecode}>Decode Message</button>
            </div>
            {decodedMessage && (
                <div>
                    <h2>Decoded Message:</h2>
                    <p>{decodedMessage}</p>
                </div>
            )}
        </div>
    );
};

export default SteganographyTool;
