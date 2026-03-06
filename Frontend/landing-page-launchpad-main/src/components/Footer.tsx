import { Link } from "react-router-dom";

const Footer = () => (
  <footer className="bg-primary text-primary-foreground">
    <div className="container py-12">
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-8">
        {/* Logo & Description */}
        <div className="col-span-2 md:col-span-1">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-8 h-8 rounded-lg bg-gold-gradient flex items-center justify-center">
              <span className="font-heading font-bold text-accent-foreground">A</span>
            </div>
            <span className="font-heading font-bold text-lg">AI-Setu ERP</span>
          </div>
          <p className="text-sm text-primary-foreground/60">
            Smart ERP for Indian retailers. AI-powered billing & store management.
          </p>
        </div>

        {/* Quick Links */}
        <div>
          <h4 className="font-heading font-bold text-sm mb-3">Quick Links</h4>
          <nav className="space-y-2">
            {[
              { label: "Features", href: "/features" },
              { label: "Pricing", href: "/pricing" },
              { label: "About Us", href: "/about" },
              { label: "Blog", href: "/blog" },
              { label: "Career", href: "/career" },
              { label: "Contact Us", href: "/contact" },
            ].map((l) => (
              <Link key={l.href} to={l.href} className="block text-sm text-primary-foreground/60 hover:text-accent transition-colors">
                {l.label}
              </Link>
            ))}
          </nav>
        </div>

        {/* Policies */}
        <div>
          <h4 className="font-heading font-bold text-sm mb-3">Policies</h4>
          <nav className="space-y-2">
            {[
              { label: "Privacy Policy", href: "/privacy" },
              { label: "Terms & Conditions", href: "/terms" },
              { label: "Refund & Cancellation", href: "/refund" },
              { label: "Data Security", href: "/data-security" },
              { label: "Support & Service", href: "/support" },
            ].map((l) => (
              <Link key={l.href} to={l.href} className="block text-sm text-primary-foreground/60 hover:text-accent transition-colors">
                {l.label}
              </Link>
            ))}
          </nav>
        </div>

        {/* Contact */}
        <div>
          <h4 className="font-heading font-bold text-sm mb-3">Contact</h4>
          <div className="space-y-2 text-sm text-primary-foreground/60">
            <p>ceo@hkdigiverse.com</p>
            <p>501-502, Silver Trade Center,<br />Mota Varachha, Surat,<br />Gujarat, India - 394101</p>
          </div>
        </div>
      </div>

      <div className="border-t border-primary-foreground/10 mt-10 pt-6 text-center text-xs text-primary-foreground/40">
        © {new Date().getFullYear()} AI-Setu ERP by Harikrushn DigiVerse LLP. All rights reserved.
      </div>
    </div>
  </footer>
);

export default Footer;
