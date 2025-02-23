import { initializeApp } from "firebase/app";
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signOut,
} from "firebase/auth";
import {
  getStorage,
  ref,
  uploadBytesResumable,
  getDownloadURL,
  deleteObject,
} from "firebase/storage";

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();
const storage = getStorage(app);

// Sign in with Google
const signInWithGoogle = async () => {
  try {
    const result = await signInWithPopup(auth, googleProvider);
    const token = await result.user.getIdToken();

    // Send token to backend for verification
    const res = await fetch("http://localhost:8080/verify-token", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token, uid: userUid }),
    });

    const data = await res.json();
    if (data.success) {
      console.log("User verified:", data);
    }
  } catch (error) {
    console.error(error);
  }
};

// Log out
const logout = () => signOut(auth);

// Function to upload file to Firebase Storage associated with the user
const uploadFile = (userId, file) => {
  const storageRef = ref(storage, `users/${userId}/files/${file.name}`);
  const uploadTask = uploadBytesResumable(storageRef, file);

  return new Promise((resolve, reject) => {
    uploadTask.on(
      "state_changed",
      (snapshot) => {
        const progress =
          (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
        console.log("Upload is " + progress + "% done");
      },
      (error) => {
        reject(error);
      },
      () => {
        getDownloadURL(uploadTask.snapshot.ref).then(resolve).catch(reject);
      }
    );
  });
};

// Function to delete the file from Firebase Storage
const deleteFile = (userId, fileName) => {
  const fileRef = ref(storage, `users/${userId}/files/${fileName}`);
  return deleteObject(fileRef);
};

export { auth, signInWithGoogle, logout, storage, uploadFile, deleteFile };
