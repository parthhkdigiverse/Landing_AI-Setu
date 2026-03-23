import { motion, Variants } from "framer-motion";
import { Check, X } from "lucide-react";
import { useEffect, useState } from "react";
import { fetchLandingPageContent } from "@/services/api";

const rowVariants: Variants = {
  hidden: { opacity: 0, x: -40 },
  visible: (i: number) => ({
    opacity: 1,
    x: 0,
    transition: { delay: i * 0.08, duration: 0.5, ease: "easeOut" },
  }),
};

const ComparisonSection = () => {
  const [rows, setRows] = useState<any[]>([]);
  const [content, setContent] = useState<any>(null); // DB static text
  const [livePreview, setLivePreview] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // 1️⃣ Fetch comparison features and content
  const fetchData = async () => {
    try {
      const [resFeatures, resContent] = await Promise.all([
        fetch("/api/comparison-features/"),
        fetchLandingPageContent(), // static titles/subtitles
      ]);

      const features = await resFeatures.json();
      setRows(features || []);
      setContent(resContent);
      setLoading(false);
    } catch (err) {
      console.error("Failed to load comparison data:", err);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // 2️⃣ Live preview listener (for admin changes)
  useEffect(() => {
    const handler = (event: any) => {
      if (event.data && event.data.source === 'django-admin') {
        if (event.data.model === 'LandingPageContent') {
          setContent((prev: any) => ({ ...prev, ...event.data.payload }));
        } else if (event.data.model === 'ComparisonFeature') {
          const item = event.data.payload;
          const pk = event.data.pk;
          setRows(prev => prev.map(r => (r.id === parseInt(pk) || r.id === pk) ? { ...r, ...item } : r));
        }
      }
    };
    window.addEventListener("message", handler);
    return () => window.removeEventListener("message", handler);
  }, []);

  if (loading) {
    return (
      <section className="py-20 lg:py-28 bg-gradient-to-b from-slate-50 to-slate-100">
        <div className="container mx-auto px-6 text-center text-gray-500">
          Loading comparison features...
        </div>
      </section>
    );
  }

  return (
    <section className="py-20 lg:py-28 bg-gradient-to-b from-slate-50 to-slate-100">
      <div className="container mx-auto px-6">
        {/* Titles */}
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900">
            {livePreview?.comparison_title || content?.comparison_title || "AI-Setu ERP vs Traditional Software"}
          </h2>
          <p className="mt-4 text-gray-500 max-w-xl mx-auto">
            {livePreview?.comparison_subtitle || content?.comparison_subtitle || "Discover why retailers are switching to AI-Setu ERP for faster, smarter store management."}
          </p>
        </div>

        {/* Comparison Table */}
        <div className="max-w-3xl mx-auto rounded-3xl overflow-hidden shadow-2xl bg-white border border-gray-200">
          {/* Header */}
          <div className="grid grid-cols-3 text-center font-semibold text-sm p-5 bg-[#1F2E4D] text-white">
            <span className="text-left">{livePreview?.comparison_column1 || "Feature"}</span>
            <span className="text-yellow-400">{livePreview?.comparison_column2 || "AI-Setu ERP"}</span>
            <span className="opacity-80">{livePreview?.comparison_column3 || "Traditional"}</span>
          </div>

          {/* Rows */}
          {(content?.comparison_features || rows).map((row, i) => (
            <motion.div
              key={row.id || i}
              custom={i}
              variants={rowVariants}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              className="grid grid-cols-3 items-center px-6 py-4 border-b last:border-none text-sm hover:bg-slate-50 transition-colors"
            >
              <span className="text-left font-medium text-gray-800">{row.feature_name}</span>

              {/* AI-Setu */}
              <span className="flex justify-center">
                {row.has_ai_setu ? (
                  <Check className="h-5 w-5 text-green-600 bg-green-100 rounded-full p-1" />
                ) : (
                  <X className="h-5 w-5 text-red-500 bg-red-100 rounded-full p-1" />
                )}
              </span>

              {/* Traditional */}
              <span className="flex justify-center">
                {row.has_traditional ? (
                  <Check className="h-5 w-5 text-green-600 bg-green-100 rounded-full p-1" />
                ) : (
                  <X className="h-5 w-5 text-red-500 bg-red-100 rounded-full p-1" />
                )}
              </span>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ComparisonSection;