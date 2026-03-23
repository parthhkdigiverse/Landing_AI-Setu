import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { CalendarCheck, Settings, Rocket } from "lucide-react";
import { fetchHowItWorks } from "@/services/api";
import { fetchLandingPageContent, LandingPageContent } from "@/services/api";

const iconMap: any = {
  calendar: CalendarCheck,
  settings: Settings,
  rocket: Rocket,
};

const HowItWorks = () => {
  const [content, setContent] = useState<LandingPageContent | null>(null);
  const [livePreview, setLivePreview] = useState<any>(null);
  const [steps, setSteps] = useState<any[]>([]);

  // Load section headings from LandingPageContent
  useEffect(() => {
    const loadContent = async () => {
      const data = await fetchLandingPageContent();
      if (data) setContent(data);
    };
    loadContent();
  }, []);

  // Fetch steps from API
  useEffect(() => {
    const loadSteps = async () => {

      const data = await fetchHowItWorks();
      setSteps(data);

    };
    loadSteps();
  }, []);

  // Live preview listener
  useEffect(() => {
    const handler = (event: any) => {
      if (event.data && event.data.source === 'django-admin') {
        if (event.data.model === 'LandingPageContent') {
          setContent((prev: any) => ({ ...prev, ...event.data.payload }));
        } else if (event.data.model === 'HowItWorksStep') {
          const item = event.data.payload;
          const pk = event.data.pk;
          setSteps(prev => prev.map(s => (s.id === parseInt(pk) || s.id === pk) ? { ...s, ...item } : s));
        }
      }
    };
    window.addEventListener("message", handler);
    return () => window.removeEventListener("message", handler);
  }, []);

  const isPreview = typeof window !== 'undefined' ? new URLSearchParams(window.location.search).get('is_preview') === '1' : false;

  return (
    <section className="py-16 lg:py-24 bg-background">
      <div className="container">
        {/* Section Header */}
        <div className="text-center mb-12">
          <span className="text-accent font-semibold text-sm uppercase tracking-wider">
            {livePreview?.howitworks_label || content?.howitworks_label || "Simple Process"}
          </span>

          <h2 className="text-3xl lg:text-4xl font-bold mt-2 text-foreground">
            {livePreview?.howitworks_title || content?.howitworks_title || "How It Works"}
          </h2>
        </div>

        {/* Steps */}
        <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          {(content?.howitworks_steps || steps).map((s, i) => {
            const Icon = iconMap[s.icon];
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.15 }}
                className="text-center relative"
              >
                <div className="w-16 h-16 rounded-2xl bg-gold-gradient flex items-center justify-center mx-auto mb-4">
                  {Icon && <Icon className="h-7 w-7 text-accent-foreground" />}
                </div>

                <span className="text-xs font-bold text-accent tracking-widest">
                  {String(s.step_number).padStart(2, "0")}
                </span>

                <h3 className="font-heading font-bold text-xl text-foreground mt-1 mb-2">
                  {s.title}
                </h3>

                <p className="text-sm text-muted-foreground">{s.description}</p>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;