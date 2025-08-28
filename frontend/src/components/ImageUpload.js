import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function ImageUpload() {
  const [image, setImage] = useState(null);
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  const onDrop = useCallback((acceptedFiles) => {
    setFile(acceptedFiles[0]);
    setImage(URL.createObjectURL(acceptedFiles[0]));
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  const handlePredict = () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    axios
      .post("http://localhost:8001/predict", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((res) => {
        const predictionData = {
          predictedClass: res.data.predictedClass,
          confidence: res.data.confidence,
          accuracy: 0.6355,
          imageUrl: image,
        };
        navigate("/result", { state: { predictionData } });
      })
      .catch((err) => console.error(err));
  };

  return (
    <div className="flex flex-col items-center p-6 w-96 mx-auto mt-10">
      {/* Drop Zone */}
      <div
        {...getRootProps()}
        className={`cursor-pointer p-10 border-2 border-dashed rounded-2xl text-center transition-all duration-300 ease-in-out
          ${isDragActive ? "border-blue-500 bg-blue-50 scale-105 shadow-xl" : "border-gray-400 bg-gray-50 hover:border-blue-400 hover:bg-blue-50"}
        `}
      >
        <input {...getInputProps()} />
        <p className="text-gray-600 font-medium">
          {isDragActive ? "Drop the image here!" : "Drag & Drop an image here, or click to select"}
        </p>
        <p className="text-sm text-gray-400 mt-1">Supports JPG, PNG</p>
      </div>

      {/* Image Preview */}
      {image && (
        <>
          <div className="mt-6">
            <img
              src={image}
              alt="preview"
              className="w-48 h-48 object-cover rounded-xl shadow-lg border border-gray-200"
            />
          </div>

          <button
            onClick={handlePredict}
            className="mt-6 px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-semibold rounded-xl shadow-md hover:shadow-lg hover:scale-105 transform transition-all duration-300"
          >
             Predict
          </button>
        </>
      )}
    </div>
  );
}
