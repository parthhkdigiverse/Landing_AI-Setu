import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useState } from "react";
import { toast } from "sonner";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!email || !password) {
      toast.error("Please fill all fields");
      return;
    }

    try {
      setLoading(true);

      const response = await fetch("http://127.0.0.1:8000/api/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        toast.success(data.message);

        localStorage.setItem("userEmail", email);

        setEmail("");
        setPassword("");

        navigate("/");
      } else {
        toast.error(data.error);
      }
    } catch (error) {
      toast.error("Server error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Header />
      <main className="min-h-[80vh] flex items-center justify-center bg-background">
        <div className="w-full max-w-sm bg-card rounded-2xl p-8 shadow-card border border-border">

          <div className="text-center mb-6">
            <div className="w-12 h-12 rounded-xl bg-hero flex items-center justify-center mx-auto mb-3">
              <span className="text-accent font-heading font-bold text-xl">A</span>
            </div>

            <h1 className="font-heading font-bold text-2xl text-foreground">
              Welcome Back
            </h1>

            <p className="text-sm text-muted-foreground">
              Login to your AI-Setu ERP account
            </p>
          </div>

          <form onSubmit={handleLogin} className="space-y-4">
            <Input
              placeholder="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <Input
              placeholder="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <Button
              type="submit"
              className="w-full bg-gold-gradient text-accent-foreground"
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