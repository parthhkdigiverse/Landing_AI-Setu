import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useState } from "react";
import { toast } from "sonner";
import { useNavigate } from "react-router-dom";
import SEO from "@/components/SEO";

import { API_BASE_URL } from "@/services/api";

const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!email || !password) {
      toast.error("Fill all fields");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch(`${API_BASE_URL}/api/login/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
      });

      const data = await res.json();

      if (res.ok) {

        // Save user info
        localStorage.setItem(
          "user",
          JSON.stringify({
            email: email,
            role: data.role
          })
        );

        toast.success("Login successful!");

        // ✅ Redirect based on role
        if (data.role === "admin") {
          navigate("/admin-dashboard");
        } else {
          navigate("/");
        }

      } else {
        toast.error(data.error || "Invalid credentials");
      }

    } catch (err) {
      console.error(err);
      toast.error("Server error");
    }

    setLoading(false);
  };

  return (
    <>
      <SEO title="Admin Login" description="Log in to your AI-Setu ERP admin dashboard to manage your retail business smarter." />
      <Header />

      <main className="min-h-[80vh] flex items-center justify-center bg-background">
        <div className="w-full max-w-sm bg-card rounded-2xl p-8 shadow-card border border-border">
          <h1 className="text-center font-bold text-2xl mb-4">
            Login to AI-Setu ERP
          </h1>

          <form onSubmit={handleLogin} className="space-y-4">
            <Input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <Input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <Button
              type="submit"
              className="w-full bg-gold-gradient text-accent-foreground font-semibold"
              disabled={loading}
            >
              {loading ? "Logging in..." : "Login"}
            </Button>
          </form>
        </div>
      </main>

      <Footer />
    </>
  );
};

export default Login;