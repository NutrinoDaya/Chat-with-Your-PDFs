import { useState } from 'react'
import FileUploader from './components/FileUploader'
import ChatBox from './components/ChatBox'
import './App.css'

function App() {
  const [docId, setDocId] = useState(null)

  return (
    <div id="root">
      <h1>Chat with your PDF</h1>
      {!docId ? (
        <FileUploader onUploadSuccess={setDocId} />
      ) : (
        <ChatBox docId={docId} />
      )}
    </div>
  )
}

export default App
