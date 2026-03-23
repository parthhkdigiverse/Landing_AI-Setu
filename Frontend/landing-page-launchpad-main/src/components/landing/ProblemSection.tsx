import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Clock, Package, TrendingDown, Users, Barcode } from "lucide-react";
import { fetchLandingPageContent, LandingPageContent, fetchProblems } from "@/services/api";

const iconMap: any = {
  clock: Clock,
  package: Package,
  "trending-down": TrendingDown,
  users: Users,
  barcode: Barcode,
};

const ProblemSection = () => {

  const [content, setContent] = useState<LandingPageContent | null>(null);
  const [livePreview, setLivePreview] = useState<any>(null);
  const [problems, setProblems] = useState<any[]>([]);

  // Load section heading from LandingPageContent
  useEffect(() => {

    const loadContent = async () => {

      const data = await fetchLandingPageContent();

      if (data) {
        setContent(data);
      }

    };

    loadContent();

  }, []);

  // Fetch problems from Django API
  useEffect(() => {

    const loadProblems = async () => {

      const data = await fetchProblems();
      setProblems(data);

    };

    loadProblems();

  }, []);

  // Live preview support
  useEffect(() => {

    const handler = (event: any) => {

      if (event.data && event.data.source === 'django-admin') {
        if (event.data.model === 'LandingPageContent') {
            setContent((prev: any) => ({ ...prev, ...event.data.payload }));
        } else if (event.data.model === 'Problem') {
            const item = event.data.payload;
            const pk = event.data.pk;
            setProblems(prev => prev.map(p => (p.id === parseInt(pk) || p.id === pk) ? { ...p, ...item } : p));
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
        <motion.div
          initial={isPreview ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.1 }}
          className="text-center mb-12"
        >

          <span className="text-accent font-semibold text-sm uppercase tracking-wider">

            {livePreview?.problem_section_label ||
              content?.problem_section_label ||
              "The Challenge"}

          </span>

          <h2 className="text-3xl lg:text-4xl font-bold mt-2 text-foreground">

            {livePreview?.problem_section_title ||
              content?.problem_section_title ||
              "Retailers Face These Daily Problems"}

          </h2>

        </motion.div>

        {/* Problem Cards */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-4xl mx-auto">

          {problems.map((p, i) => {

            const Icon = iconMap[p.icon];

            return (

              <motion.div
                key={i}
                initial={isPreview ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.1 }}
                transition={{ delay: isPreview ? 0 : i * 0.1 }}
                className="bg-card rounded-xl p-6 shadow-card border border-border hover:shadow-card-hover transition-shadow"
              >

                <div className="w-10 h-10 rounded-lg bg-destructive/10 flex items-center justify-center mb-4">
                  {Icon && <Icon className="h-5 w-5 text-destructive" />}
                </div>

                <h3 className="font-heading font-bold text-foreground mb-1">
                  {p.title}
                </h3>

                <p className="text-sm text-muted-foreground">
                  {p.description}
                </p>

              </motion.div>

            );

          })}

        </div>

      </div>

    </section>
  );
};

export default ProblemSection;