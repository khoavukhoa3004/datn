
import Editor from '@monaco-editor/react';


export default function CodeEditor() {
  return (
    <div>
      <Editor 
        height="90vh" 
        defaultLanguage="javascript" 
        defaultValue="// some comment"
      />
    </div>
  )
}