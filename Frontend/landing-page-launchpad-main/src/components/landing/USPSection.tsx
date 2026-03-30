import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";
import DynamicIcon from "@/components/DynamicIcon";
import aiScan from "@/assets/ai-scan.jpg";
import { fetchUSPFeatures } from "@/services/api";
import { fetchLandingPageContent, LandingPageContent } from "@/services/api";

const USPSection = () => {
  const [content, setContent] = useState<LandingPageContent | null>(null);
  const [livePreview, setLivePreview] = useState<any>(null);
  const [features, setFeatures] = useState<any[]>([]);

  // Load section heading/subheading from LandingPageContent
  useEffect(() => {
    const loadContent = async () => {
      const data = await fetchLandingPageContent();
      if (data) setContent(data);
    };
    loadContent();
  }, []);

  // Fetch features from API
  useEffect(() => {
    const loadFeatures = async () => {
      try {
        const res = await fetch("/api/usp-features/");
        const data = await res.json();
        setFeatures(data);
      } catch (err) {
        console.error("USP feature load error", err);
      }
    };
    loadFeatures();
  }, []);

  // Live preview listener
  useEffect(() => {
    const handler = (event: any) => {
      if (event.data && event.data.source === 'django-admin') {
        if (event.data.model === 'LandingPageContent' || event.data.model === 'USPContent') {
          setContent((prev: any) => ({ ...prev, ...event.data.payload }));
        } else if (event.data.model === 'USPFeature') {
          const item = event.data.payload;
          const pk = event.data.pk;
          setFeatures(prev => prev.map(f => (f.id === parseInt(pk) || f.id === pk) ? { ...f, ...item } : f));
        }
      }
    };
    window.addEventListener("message", handler);
    return () => window.removeEventListener("message", handler);
  }, []);

  const isPreview = typeof window !== 'undefined' ? new URLSearchParams(window.location.search).get('is_preview') === '1' : false;

  return (
    <section className="relative py-16 lg:py-32 bg-gradient-to-br from-[#1F2E4D] via-[#2D3748] to-[#1A202C] text-primary-foreground overflow-hidden">
      <div className="container relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">

          {/* LEFT CONTENT */}
          <motion.div
            initial={isPreview ? { opacity: 1, x: 0 } : { opacity: 0, x: -40 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.7 }}
          >
            {/* Section Label */}
            <div className="flex justify-center lg:justify-start">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-accent/20 rounded-full border border-accent/30 mb-6">
                <Sparkles className="h-4 w-4 text-accent" />
                <span className="text-accent font-semibold text-sm uppercase tracking-wider">
                  {livePreview?.usp_badge_text ||
                    content?.usp_badge_text ||
                    "AI-Powered (Beta Feature)"}
                </span>
              </div>
            </div>

            {/* Heading */}
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold leading-tight mb-6 text-center lg:text-left">
              {livePreview?.usp_title ||
                content?.usp_title ||
                "No Barcode? No Problem."}
            </h2>

            {/* Subheading */}
            <p className="text-lg text-gray-300 mb-10 max-w-md leading-relaxed mx-auto lg:mx-0 text-center lg:text-left">
              {livePreview?.usp_description ||
                content?.usp_description ||
                "Our AI technology identifies products from photos — just snap and bill."}
            </p>

            {/* Features */}
            <div className="space-y-4">
              {(content?.usp_features || features).map((f, i) => (
                <motion.div
                  key={i}
                  whileHover={{ scale: 1.04, x: 8 }}
                  className="group flex items-start gap-4 p-4 rounded-xl bg-white/5 backdrop-blur-lg border border-white/10 hover:border-accent/30 hover:bg-accent/5 transition-all duration-300"
                >
                  <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-accent to-yellow-500 flex items-center justify-center">
                    <DynamicIcon name={f.icon} className="h-6 w-6 text-[#1F2E4D]" />
                  </div>

                  <div>
                    <h3 className="font-semibold text-white mb-1">{f.title}</h3>
                    <p className="text-sm text-gray-400">{f.description}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* RIGHT IMAGE */}
          <motion.div
            initial={isPreview ? { opacity: 1, x: 0 } : { opacity: 0, x: 40 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="relative flex justify-center"
          >
            <div className="relative w-full max-w-[420px] group">
              <div className="absolute -inset-1 bg-gradient-to-r from-accent to-yellow-500 rounded-3xl blur opacity-25 group-hover:opacity-40 transition duration-1000 group-hover:duration-200"></div>
              <img
                src={aiScan}
                alt="AI Product Scanning"
                className="relative rounded-2xl shadow-2xl w-full object-cover transform hover:scale-[1.02] transition-transform duration-500"
              />
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default USPSection;