import { motion } from "framer-motion";
import { Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { fetchLandingPageContent } from "@/services/api";

const PricingSection = () => {

  const navigate = useNavigate();

  const [content, setContent] = useState<any>(null);

  // Fetch database content
  useEffect(() => {
    const loadContent = async () => {
      const data = await fetchLandingPageContent();
      if (data) {
        setContent(data);
      }
    };
    loadContent();
  }, []);

  // Live preview listener
  useEffect(() => {
    const handler = (event: any) => {
      if (event.data && event.data.source === 'django-admin') {
        if (event.data.model === 'LandingPageContent' || event.data.model === 'PricingContent') {
          const payload = event.data.payload;
          setContent((prev: any) => ({
            ...prev,
            ...payload
          }));
        }
      }
    };

    window.addEventListener("message", handler);
    return () => window.removeEventListener("message", handler);
  }, []);

  const featuresList = content?.pricing_features?.length > 0 
    ? content.pricing_features.map((f: any) => f.title)
    : [
        content?.pricing_feature1 || "Full Access to All Modules",
        content?.pricing_feature2 || "POS Billing + Inventory",
        content?.pricing_feature3 || "CRM & Loyalty Programs",
        content?.pricing_feature4 || "Accounting & Reports",
        content?.pricing_feature5 || "Employee Management",
        content?.pricing_feature6 || "Setup & Training Support",
        content?.pricing_feature7 || "24/7 Customer Support",
        content?.pricing_feature8 || "AI Photo Billing",
      ];

  return (
    <section id="pricing" className="py-16 lg:py-24 bg-background">

      <div className="container">

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >

          <span className="text-accent font-semibold text-sm uppercase tracking-wider">
            {content?.pricing_label ||
             content?.pricing_label ||
             "Pricing"}
          </span>

          <h2 className="text-3xl lg:text-4xl font-bold mt-2 text-foreground">
            {content?.pricing_title ||
             content?.pricing_title ||
             "Simple & Transparent Pricing"}
          </h2>

        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-md mx-auto bg-card rounded-2xl p-8 shadow-card border-2 border-accent"
        >

          <div className="text-center mb-6">

            <p className="text-muted-foreground text-sm mb-2">
              {content?.pricing_plan_name ||
               content?.pricing_plan_name ||
               "All-Inclusive Package"}
            </p>

            <div className="flex flex-col items-center justify-center gap-1">

              <span className="text-muted-foreground line-through text-lg font-medium tracking-wide">
                {content?.pricing_old_price ||
                 content?.pricing_old_price ||
                 "₹29,999"}
              </span>

              <div className="flex items-baseline gap-1 mt-1">

                <span className="text-5xl font-extrabold text-foreground">
                  {content?.pricing_price ||
                   content?.pricing_price ||
                   "₹12,000"}
                </span>

                <span className="text-muted-foreground text-sm">
                  {content?.pricing_price_suffix ||
                   content?.pricing_price_suffix ||
                   "+ GST"}
                </span>

              </div>

            </div>

          </div>

          <div className="space-y-3 mb-8">
            {featuresList.map((f, index) => (
              <div key={index} className="flex items-center gap-3">
                <Check className="h-4 w-4 text-accent flex-shrink-0" />
                <span className="text-sm text-foreground">{f}</span>
              </div>
            ))}
          </div>

          <Button
            onClick={() => navigate("/pricing-signup")}
            className="w-full bg-gold-gradient text-accent-foreground font-semibold hover:opacity-90 text-base py-6"
          >
            Get Started Today
          </Button>

        </motion.div>

      </div>

    </section>
  );
};

export default PricingSection;