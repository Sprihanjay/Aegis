import React, { useState, useEffect } from "react";
import {
  signInWithGoogle,
  logout,
  auth,
  storage,
  uploadFile,
  deleteFile,
} from "../firebase/firebase";
import { onAuthStateChanged } from "firebase/auth";
import { ref, listAll, getDownloadURL } from "firebase/storage";
import { FaGoogle } from "react-icons/fa";
import background1 from "../assets/background1.jpg";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const navigate = useNavigate();

  const [user, setUser] = useState(null);
  const [file, setFile] = useState(null);
  const glassStyle = {
    background: "rgba(109, 108, 108, 0.7)",
    borderRadius: "16px",
    boxShadow: "0 4px 30px rgba(0, 0, 0, 0.1)",
    backdropFilter: "blur(5px)",
    WebkitBackdropFilter: "blur(5px)",
    border: "1px solid rgba(144, 144, 144, 0.49)",
  };
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [fileUrl, setFileUrl] = useState("");

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      setUser(currentUser);

      if (currentUser) {
        fetchUserFiles(currentUser.uid);
      }
    });
    return () => unsubscribe();
  }, []);

  const fetchUserFiles = (userId) => {
    const storageRef = ref(storage, `users/${userId}/files/`);
    listAll(storageRef)
      .then((res) => {
        const filesPromises = res.items.map(async (item) => {
          const url = await getDownloadURL(item);
          return { name: item.name, url };
        });
        Promise.all(filesPromises).then((files) => setUploadedFiles(files));
      })
      .catch((error) => console.error("Error fetching files: ", error));
  };

  const handleFileChange = (event) => setFile(event.target.files[0]);

  const handleUpload = () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }

    if (user) {
      uploadFile(user.uid, file)
        .then((downloadURL) => {
          setFileUrl(downloadURL);
          fetchUserFiles(user.uid);
          navigate("/title-screen");
        })
        .catch((error) => {
          console.error("Upload failed", error);
        });
    }
  };

  const handleDelete = (fileName) => {
    if (user) {
      deleteFile(user.uid, fileName)
        .then(() => fetchUserFiles(user.uid))
        .catch((error) => console.error("Error deleting file:", error));
    }
  };

  const handleLogout = () => {
    logout();
  };

  return (
    <div
      style={{ backgroundImage: `url(${background1})` }}
      className="min-h-screen flex items-center justify-center bg-cover bg-center"
    >
      <div
        style={glassStyle}
        className="bg-gray-700 bg-opacity-50 rounded-2xl shadow-lg p-10 w-96"
      >
        {user ? (
          <div className="text-white text-center">
            <h2 className="text-2xl font-bold mb-4">
              Welcome, {user.displayName}
            </h2>
            <img
              src={user.photoURL}
              alt="User"
              className="w-20 h-20 rounded-full mx-auto mb-4"
            />
            <p>{user.email}</p>
            <p className="mt-4">
              Please upload the balance sheet, shareholder equity statement, and
              cashflow statement.
            </p>
            <input
              type="file"
              onChange={handleFileChange}
              className="block w-full mt-4 text-gray-700 bg-white border border-gray-300 rounded-md focus:ring focus:ring-yellow-400"
            />
            <button
              onClick={handleUpload}
              className="w-full mt-4 py-2 bg-yellow-400 hover:bg-yellow-300 rounded-md text-black font-bold"
            >
              Upload File
            </button>
            <button
              onClick={handleLogout}
              className="w-full mt-2 py-2 bg-red-500 hover:bg-red-400 rounded-md text-white font-bold"
            >
              Logout
            </button>
            {uploadedFiles.length > 0 && (
              <div className="mt-6">
                <h3 className="text-xl font-semibold">Your uploaded files:</h3>
                {uploadedFiles.map((file, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between mt-2"
                  >
                    <a
                      href={file.url}
                      className="text-yellow-400 hover:underline"
                    >
                      {file.name}
                    </a>
                    <button
                      onClick={() => handleDelete(file.name)}
                      className="bg-red-500 hover:bg-red-400 text-white px-2 py-1 rounded-md"
                    >
                      Delete
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        ) : (
          <div className="text-center text-white">
            <h2 className="text-2xl font-bold mb-4">Create an account</h2>
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="block w-full mb-4 p-2 rounded-md text-gray-700 bg-white border border-gray-300"
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="block w-full mb-4 p-2 rounded-md text-gray-700 bg-white border border-gray-300"
            />
            <button className="w-full py-2 bg-yellow-400 hover:bg-yellow-300 rounded-md text-black font-bold mb-4">
              Sign Up
            </button>
            <div className="flex items-center justify-center mb-4">
              <hr className="w-16 border-gray-300" />
              <span className="px-3 text-gray-300">or</span>
              <hr className="w-16 border-gray-300" />
            </div>
            <button
              onClick={signInWithGoogle}
              className="flex items-center justify-center w-full py-2 bg-white hover:bg-gray-200 text-black rounded-md"
            >
              <FaGoogle className="mr-2" />
              Sign in with Google
            </button>
            <div className="mt-4">
              <p>
                Have an account?{" "}
                <a
                  href="#"
                  className="font-bold text-yellow-400 hover:underline"
                >
                  Sign in
                </a>
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Login;
