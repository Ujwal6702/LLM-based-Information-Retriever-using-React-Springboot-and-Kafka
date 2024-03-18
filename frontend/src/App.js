import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from './pages/login-signup/login-signup';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
