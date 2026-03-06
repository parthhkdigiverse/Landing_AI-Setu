import { motion } from "framer-motion";
import { Check, X } from "lucide-react";

const rows = [
  { feature: "AI Photo Billing", us: true, them: false },
  { feature: "Simple Interface", us: true, them: false },
  { feature: "One Package Pricing", us: true, them: false },
  { feature: "Retail-Focused", us: true, them: false },
  { feature: "GST Ready", us: true, them: true },
  { feature: "Cloud-Based", us: true, them: false },
  { feature: "24/7 Support", us: true, them: false },
];

const ComparisonSection = () => (
  <section className="py-16 lg:py-24 bg-secondary">
    <div className="container">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center mb-12"
      >
        <h2 className="text-3xl lg:text-4xl font-bold text-foreground">
          AI-Setu ERP vs Traditional Software
        </h2>
      </motion.div>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="max-w-2xl mx-auto bg-card rounded-2xl shadow-card overflow-hidden border border-border"
      >
        <div className="grid grid-cols-3 text-center font-heading font-bold text-sm p-4 bg-primary text-primary-foreground">
          <span className="text-left">Feature</span>
          <span>AI-Setu ERP</span>
          <span>Traditional</span>
        </div>
        {rows.map((r, i) => (
          <div key={r.feature} className={`grid grid-cols-3 text-center text-sm p-4 ${i % 2 === 0 ? "bg-card" : "bg-secondary"}`}>
            <span className="text-left font-medium text-foreground">{r.feature}</span>
            <span>{r.us ? <Check className="h-5 w-5 text-accent mx-auto" /> : <X className="h-5 w-5 text-destructive mx-auto" />}</span>
            <span>{r.them ? <Check className="h-5 w-5 text-accent mx-auto" /> : <X className="h-5 w-5 text-destructive mx-auto" />}</span>
          </div>
        ))}
      </motion.div>
    </div>
  </section>
);

export default ComparisonSection;
