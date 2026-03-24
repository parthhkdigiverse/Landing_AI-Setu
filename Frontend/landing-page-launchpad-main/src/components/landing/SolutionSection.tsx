import { useEffect, useState } from "react";
import { motion, Variants } from "framer-motion";
import {
  CreditCard,
  Package,
  Heart,
  Calculator,
  UserCheck,
  BarChart3,
  Loader2,
} from "lucide-react";
import { fetchLandingPageContent, LandingPageContent } from "@/services/api";

const iconMap: any = {
  "credit-card": CreditCard,
  package: Package,
  heart: Heart,
  calculator: Calculator,
  "user-check": UserCheck,
  "bar-chart": BarChart3,
};

const containerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1, delayChildren: 0.3 },
  },
};

const cardVariants: Variants = {
  hidden: { opacity: 0, y: 50, scale: 0.8 },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: { type: "spring", stiffness: 100, damping: 12 },
  },
};

const SolutionSection = () => {
  const [content, setContent] = useState<LandingPageContent | null>(null);
  const [livePreview, setLivePreview] = useState<any>(null);
  const [solutions, setSolutions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // Load section heading from LandingPageContent
  useEffect(() => {
    const loadContent = async () => {
      const data = await fetchLandingPageContent();
      if (data) setContent(data);
    };
    loadContent();
  }, []);

  // Fetch solutions from Django API
  useEffect(() => {
    const loadSolutions = async () => {
      try {
        setLoading(true);
        const res = await fetch("/api/features/");
        const data = await res.json();
        setSolutions(data);
      } catch (err) {
        console.error("Failed to load solutions", err);
      } finally {
        setLoading(false);
      }
    };
    loadSolutions();
  }, []);

  // Live preview listener
  useEffect(() => {
    const handler = (event: any) => {
      if (event.data && event.data.source === 'django-admin') {
        if (event.data.model === 'LandingPageContent' || event.data.model === 'SolutionContent') {
          setContent((prev: any) => ({ ...prev, ...event.data.payload }));
        } else if (event.data.model === 'Feature') {
          const item = event.data.payload;
          const pk = event.data.pk;
          setSolutions(prev => prev.map(s => (s.id === parseInt(pk) || s.id === pk) ? { ...s, ...item } : s));
        }
      }
    };
    window.addEventListener("message", handler);
    return () => window.removeEventListener("message", handler);
  }, []);

  const isPreview = typeof window !== 'undefined' ? new URLSearchParams(window.location.search).get('is_preview') === '1' : false;

  return (
    <section 
      id="features" // CRITICAL: This allows the header link to find this section
      className="relative py-16 lg:py-24 bg-gradient-to-br from-background via-secondary to-muted overflow-hidden min-h-[600px]"
    >
      <div className="container relative z-10">
        
        {/* Section Header */}
        <motion.div
          initial={isPreview ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.1 }}
          className="text-center mb-16"
        >
          <span className="inline-block px-4 py-2 bg-accent text-accent-foreground font-semibold text-sm uppercase tracking-wider rounded-full shadow-lg mb-4">
            {livePreview?.solution_section_label ||
              content?.solution_section_label ||
              "The Solution"}
          </span>

          <h2 className="text-4xl lg:text-5xl font-bold text-foreground leading-tight">
            {livePreview?.solution_section_title ||
              content?.solution_section_title ||
              "One Smart ERP For Complete Store Management"}
          </h2>
        </motion.div>

        {/* Loading State or Solution Cards */}
        {loading ? (
          <div className="flex flex-col items-center justify-center py-20">
            <Loader2 className="h-10 w-10 animate-spin text-primary mb-4" />
            <p className="text-muted-foreground animate-pulse">Loading features...</p>
          </div>
        ) : (
          <motion.div
            variants={containerVariants}
            initial={isPreview ? "visible" : "hidden"}
            whileInView="visible"
            viewport={{ once: true, amount: 0.1 }}
            className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8"
          >
            {(content?.features || solutions).map((s, i) => {
              const Icon = iconMap[s.icon];
              return (
                <motion.div
                  key={s.id || i}
                  variants={cardVariants}
                  className="group bg-card rounded-2xl p-8 shadow-card border border-border hover:shadow-card-hover transition-all"
                >
                  <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-900 flex items-center justify-center mb-6">
                    {Icon && <Icon className="h-8 w-8 text-white" />}
                  </div>

                  <h3 className="font-bold text-xl text-foreground mb-3">
                    {s.title}
                  </h3>

                  <p className="text-muted-foreground">{s.description}</p>
                </motion.div>
              );
            })}
          </motion.div>
        )}
      </div>
    </section>
  );
};

export default SolutionSection;