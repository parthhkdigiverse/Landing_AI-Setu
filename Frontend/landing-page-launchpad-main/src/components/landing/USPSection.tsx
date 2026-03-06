import { motion } from "framer-motion";
import { Camera, Cpu, Zap } from "lucide-react";
import aiScan from "@/assets/ai-scan.jpg";

const features = [
  { icon: Camera, title: "Photo-Based Product Detection" },
  { icon: Cpu, title: "AI Auto Identify Product" },
  { icon: Zap, title: "Add Directly to Bill" },
];

const USPSection = () => (
  <section className="py-16 lg:py-24 bg-hero text-primary-foreground overflow-hidden">
    <div className="container grid lg:grid-cols-2 gap-12 items-center">
      <motion.div
        initial={{ opacity: 0, x: -30 }}
        whileInView={{ opacity: 1, x: 0 }}
        viewport={{ once: true }}
      >
        <span className="text-accent font-semibold text-sm uppercase tracking-wider">AI-Powered</span>
        <h2 className="text-3xl lg:text-4xl font-bold mt-2 mb-6">
          No Barcode? <span className="text-gradient-gold">No Problem.</span>
        </h2>
        <p className="text-primary-foreground/70 mb-8 max-w-md">
          Our AI technology identifies products from photos — just snap and bill. No barcode scanner needed.
        </p>
        <div className="space-y-4">
          {features.map((f) => (
            <div key={f.title} className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-accent/20 flex items-center justify-center">
                <f.icon className="h-5 w-5 text-accent" />
              </div>
              <span className="font-semibold">{f.title}</span>
            </div>
          ))}
        </div>
      </motion.div>
      <motion.div
        initial={{ opacity: 0, x: 30 }}
        whileInView={{ opacity: 1, x: 0 }}
        viewport={{ once: true }}
      >
        <img src={aiScan} alt="AI Product Scanning" className="rounded-2xl shadow-2xl w-full max-w-md mx-auto" />
      </motion.div>
    </div>
  </section>
);

export default USPSection;
