import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ImageUpload from "./components/ImageUpload";
import Result from "./components/Result";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ImageUpload />} />
        <Route path="/result" element={<Result />} />
      </Routes>
    </Router>
  );
}
