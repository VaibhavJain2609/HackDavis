import { AuthProvider } from "@propelauth/react";
import React from "react";
import ReactDOM from "react-dom";
import YourApp from "./components/YourApp";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
    <AuthProvider authUrl={process.env.REACT_APP_AUTH_URL}>
        <YourApp />
    </AuthProvider>,
    document.getElementById("root")
);