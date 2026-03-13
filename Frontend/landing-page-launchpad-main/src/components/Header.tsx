import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import DemoForm from "@/components/DemoForm";
import { fetchLandingPageContent, LandingPageContent } from "@/services/api";

const Header = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [demoOpen, setDemoOpen] = useState(false);
  const [content, setContent] = useState<LandingPageContent | null>(null);

  useEffect(() => {
    const loadContent = async () => {
      const data = await fetchLandingPageContent();
      if (data) setContent(data);
    };
    loadContent();
  }, []);


  const navItems = [
    { label: "Features", href: "/features" },
    { label: "Pricing", href: "/pricing" },
    { label: "Referral Program", href: "/referral" },
    { label: "Login", href: "https://ai-setu.com/auth/signin" },
    // { label: "Login", href: "/login" },

  ];

  return (
    <>
      <header className="sticky top-0 z-50 bg-card/80 backdrop-blur-lg border-b border-border">
        <div className="container flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-9 h-9 rounded-lg bg-hero flex items-center justify-center">
              <span className="text-accent font-heading font-bold text-lg">A</span>
            </div>
            <span className="font-heading font-bold text-xl text-foreground">AI-Setu ERP</span>
          </Link>

          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center gap-6">
            {navItems.map((item) => (
              <Link
                key={item.href}
                to={item.href}
                className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
              >
                {item.label}
              </Link>
            ))}
            <Button
              onClick={() => setDemoOpen(true)}
              className="bg-gold-gradient text-accent-foreground font-semibold
                transition-all duration-200
                hover:scale-105 hover:shadow-[0_0_20px_rgba(255,200,50,0.5)] hover:opacity-100
                active:scale-95"
            >
              {content?.primary_cta_text || "Get A Free Demo"}
            </Button>
          </nav>

          {/* Mobile Toggle */}
          <button className="md:hidden text-foreground" onClick={() => setMobileOpen(!mobileOpen)}>
            {mobileOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Nav */}
        {mobileOpen && (
          <nav className="md:hidden bg-card border-b border-border px-6 pb-4 space-y-3">
            {navItems.map((item) => (
              <Link
                key={item.href}
                to={item.href}
                className="block text-sm font-medium text-muted-foreground hover:text-foreground"
                onClick={() => setMobileOpen(false)}
              >
                {item.label}
              </Link>
            ))}
            <Button
              onClick={() => { setDemoOpen(true); setMobileOpen(false); }}
              className="w-full bg-gold-gradient text-accent-foreground font-semibold
                transition-all duration-200
                hover:scale-105 hover:shadow-[0_0_20px_rgba(255,200,50,0.5)]
                active:scale-95"
            >
              {content?.primary_cta_text || "Get A Free Demo"}
            </Button>
          </nav>
        )}
      </header>

      {/* Demo Dialog Modal */}
      <Dialog open={demoOpen} onOpenChange={setDemoOpen}>
        <DialogContent className="sm:max-w-sm bg-card border border-border">
          <DialogHeader>
            <DialogTitle className="font-heading font-bold text-2xl text-foreground">
              Book A Free Demo
            </DialogTitle>
            <DialogDescription className="text-sm text-muted-foreground">
              Fill the form and our team will contact you shortly.
            </DialogDescription>
          </DialogHeader>
          <DemoForm />
        </DialogContent>
      </Dialog>
    </>
  );
};

export default Header;

