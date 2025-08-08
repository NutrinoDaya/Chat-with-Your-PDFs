export default function Message({ sender, text }) {
  return (
    <div className={`message ${sender}`}>
      {text}
    </div>
  );
}
