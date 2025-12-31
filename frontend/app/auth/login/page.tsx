"use client";

import { useState } from "react";
import { login } from "@/services/auth.service";
import { setToken } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
  setError("");

  try {
    const res = await login(email, password);

    console.log("login response from backend:", res);

    if (!res?.access_token) {
      setError("unexpected auth response");
      return;
    }

    setToken(res.access_token);
    router.push("/dashboard");
  } catch (err: any) {
    if (err.response?.status === 400) {
      setError("invalid credentials");
    } else {
      setError("login failed");
    }
  }
};


  return (
    <div className="max-w-sm mx-auto mt-32">
      <h1 className="text-xl font-semibold mb-4">Login</h1>

      <input
        placeholder="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      {error && <p className="text-red-500">{error}</p>}

      <button onClick={handleLogin}>login</button>
    </div>
  );
}
