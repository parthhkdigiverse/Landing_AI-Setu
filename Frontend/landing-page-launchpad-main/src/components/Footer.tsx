import { Link } from "react-router-dom";
import logo from "@/assets/logo_2.png";
import { useEffect, useState } from "react";
import { API_BASE_URL } from "@/services/api";

const Footer = () => {

  const [footer, setFooter] = useState<any>(null);
  const [livePreview, setLivePreview] = useState<any>(null);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/footer/`)
      .then((res) => res.json())
      .then((data) => setFooter(data))
      .catch((err) => console.log(err));
  }, []);

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      // INIT INSTANT SNAP
      if (event.data && event.data.source === 'django-admin-init' && event.data.target === 'footer') {
         const footerEl = document.getElementById("master-footer");
         if (footerEl) footerEl.scrollIntoView({ behavior: 'instant', block: 'center' });
         return;
      }

      if (event.data && event.data.source === 'django-admin') {
        const payload = event.data.payload;

        // Determine if this payload has footer fields. 
        if (payload.email !== undefined || payload.address !== undefined || payload.description !== undefined) {
          
          let quick_links = footer?.quick_links || [];
          let policies = footer?.policies || [];

          try {
            if (payload.quick_links) quick_links = JSON.parse(payload.quick_links);
          } catch(e) {}
          
          try {
            if (payload.policies) policies = JSON.parse(payload.policies);
          } catch(e) {}

          setLivePreview({
            description: payload.description,
            email: payload.email,
            address: payload.address,
            phone: payload.phone,
            quick_links: quick_links,
            policies: policies,
          });
        }
      }
    };
    
    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, [footer]);

  const displayData = livePreview || footer;

  if (!displayData) return null;

  return (
    <footer id="master-footer" className="bg-primary text-primary-foreground">
      <div className="container py-12">
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-8">

          {/* Logo & Description */}
          <div className="col-span-2 md:col-span-1">
            <div className="flex items-center gap-2 mb-3">
              <img
                src={logo}
                alt="AI-Setu ERP"
                className="h-10 w-auto object-contain"
              />
            </div>

            <p className="text-sm text-primary-foreground/60 whitespace-pre-wrap">
              {displayData.description}
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-heading font-bold text-sm mb-3">Quick Links</h4>
            <nav className="space-y-2">
              {displayData.quick_links?.map((l: any, i: number) => (
                <Link
                  key={l.href || i}
                  to={l.href || "#"}
                  className="block text-sm text-primary-foreground/60 hover:text-accent transition-colors"
                >
                  {l.label}
                </Link>
              ))}
            </nav>
          </div>

          {/* Policies */}
          <div>
            <h4 className="font-heading font-bold text-sm mb-3">Policies</h4>
            <nav className="space-y-2">
              {displayData.policies?.map((l: any, i: number) => (
                <Link
                  key={l.href || i}
                  to={l.href || "#"}
                  className="block text-sm text-primary-foreground/60 hover:text-accent transition-colors"
                >
                  {l.label}
                </Link>
              ))}
            </nav>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-heading font-bold text-sm mb-3">Contact</h4>
            <div className="space-y-2 text-sm text-primary-foreground/60">
              <p>{displayData.email}</p>
              <p dangerouslySetInnerHTML={{ __html: displayData.address }} />
              <p>{displayData.phone}</p>
            </div>
          </div>

        </div>

        <div className="border-t border-primary-foreground/10 mt-10 pt-6 text-center text-xs text-primary-foreground/40">
          © {new Date().getFullYear()} AI-Setu ERP by Harikrushn DigiVerse LLP. All rights reserved.
        </div>

      </div>
    </footer>
  );
};

export default Footer;