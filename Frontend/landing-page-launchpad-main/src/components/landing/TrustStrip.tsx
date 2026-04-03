import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import DynamicIcon from "@/components/DynamicIcon";
import { fetchLandingPageContent, LandingPageContent } from "@/services/api";

const defaultItems = [
  "Made for Indian Retailers",
  "GST Ready",
  "Secure Cloud Data",
  "24/7 Support",
];

interface TrustStripProps {
  content?: LandingPageContent | null;
}

const TrustStrip = ({ content: propContent }: TrustStripProps) => {
  const [content, setContent] = useState<LandingPageContent | null>(propContent || null);
  const [livePreview, setLivePreview] = useState<any>(null);

  // Sync state if prop changes
  useEffect(() => {
    if (propContent) {
      setContent(propContent);
    }
  }, [propContent]);

  useEffect(() => {
    if (propContent) return;

    const loadContent = async () => {
      const data = await fetchLandingPageContent();
      if (data) {
        setContent(data);
      }
    };
    loadContent();
  }, [propContent]);

  useEffect(() => {
    const handler = (event: any) => {
      if (event.data && event.data.source === 'django-admin') {
        setLivePreview(event.data.payload);
      }
    };
    window.addEventListener("message", handler);
    return () => window.removeEventListener("message", handler);
  }, []);

  const items = (livePreview?.trust_items || content?.trust_items || []).filter((item: any) => item.is_active !== false);

  const displayItems = items.length > 0 ? items : defaultItems.map((text, i) => ({
    title: text,
    icon: i === 0 ? 'indian-rupee' : i === 1 ? 'shield-check' : i === 2 ? 'cloud' : 'headphones'
  }));

  return (
    <section id="trusted-retailers" className="border-y border-border bg-gradient-to-r from-background via-secondary/30 to-background">
      <div className="container py-5">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {displayItems.map((item: any, i: number) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.08 }}
              className="flex items-center gap-3 justify-center px-4 py-3 rounded-xl
              bg-card border border-border shadow-sm
              hover:shadow-card-hover hover:border-accent/30 transition-all duration-200 group"
            >
              <div
                className={`p-2 rounded-lg bg-accent/10 text-primary group-hover:scale-110 transition-transform duration-200`}
              >
                <DynamicIcon name={item.icon} className="h-4 w-4" />
              </div>
              <span className="text-sm font-semibold text-foreground">
                {item.title}
              </span>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default TrustStrip;