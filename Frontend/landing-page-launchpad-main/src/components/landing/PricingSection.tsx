import { motion } from "framer-motion";
import { Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

const features = [
  "Full Access to All Modules",
  "POS Billing + Inventory",
  "CRM & Loyalty Programs",
  "Accounting & Reports",
  "Employee Management",
  "Setup & Training Support",
  "24/7 Customer Support",
  "AI Photo Billing",
];

const PricingSection = () => {
  const navigate = useNavigate();
  return (
    <section id="pricing" className="py-16 lg:py-24 bg-background">
      <div className="container">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <span className="text-accent font-semibold text-sm uppercase tracking-wider">Pricing</span>
          <h2 className="text-3xl lg:text-4xl font-bold mt-2 text-foreground">Simple & Transparent Pricing</h2>
        </motion.div>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-md mx-auto bg-card rounded-2xl p-8 shadow-card border-2 border-accent"
        >
          <div className="text-center mb-6">
            <p className="text-muted-foreground text-sm mb-2">All-Inclusive Package</p>
            <div className="flex flex-col items-center justify-center gap-1">
              <span className="text-muted-foreground line-through text-lg font-medium tracking-wide">₹29,999</span>
              <div className="flex items-baseline gap-1 mt-1">
                <span className="text-5xl font-extrabold text-foreground">₹12,000</span>
                <span className="text-muted-foreground text-sm">+ GST</span>
              </div>
            </div>
          </div>
          <div className="space-y-3 mb-8">
            {features.map((f) => (
              <div key={f} className="flex items-center gap-3">
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
