// frontend/src/App.tsx
import { useState } from 'react';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string>('');
  const [labels, setLabels] = useState<any[]>([]);

  const handleUpload = async () => {
    if (!file) return;

    setStatus('Uploading...');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch("https://ktkkrv3a00.execute-api.us-east-1.amazonaws.com/Prod/upload", {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      setStatus('Processing complete!');
      setLabels(result.labels || []);
    } catch (err) {
      console.error(err);
      setStatus('Error during upload.');
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Image Rekognition</h1>
      <input type="file" accept="image/*" onChange={e => setFile(e.target.files?.[0] || null)} />
      <button onClick={handleUpload} disabled={!file}>Upload</button>
      <p>{status}</p>

      {labels.length > 0 && (
        <ul>
          {labels.map((label, i) => (
            <li key={i}>{label.Name} - {(label.Confidence).toFixed(1)}%</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;