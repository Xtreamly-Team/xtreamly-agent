// Import the functions you need from the SDKs you need
import {initializeApp} from "firebase/app";
import {getAnalytics} from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyAywXpowBLpN6x5YdbO_gBfjoAV-pIqf98",
    authDomain: "xtreamly-906e5.firebaseapp.com",
    projectId: "xtreamly-906e5",
    storageBucket: "xtreamly-906e5.appspot.com",
    messagingSenderId: "427046412977",
    appId: "1:427046412977:web:e64043690b43af96057890",
    measurementId: "G-WL8DQNW1VL"
};

export const app = initializeApp(firebaseConfig);

export function initializeGA() {
    getAnalytics(app);
}
