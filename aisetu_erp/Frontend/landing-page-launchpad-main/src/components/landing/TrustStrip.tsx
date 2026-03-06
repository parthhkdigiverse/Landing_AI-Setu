import { motion } from "framer-motion";
import { ShieldCheck, IndianRupee, Cloud, Headphones } from "lucide-react";

const items = [
  { icon: IndianRupee, label: "Made for Indian Retailers", color: "text-yellow-400" },
  { icon: ShieldCheck, label: "GST Ready", color: "text-green-400" },
  { icon: Cloud, label: "Secure Cloud Data", color: "text-blue-400" },
  { icon: Headphones, label: "24/7 Support", color: "text-purple-400" },
];

const TrustStrip = () => (
  <section className="border-y border-border bg-gradient-to-r from-background via-secondary/30 to-background">
    <div className="container py-5">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {items.map((item, i) => (
          <motion.div
            key={item.label}
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.08 }}
            className="flex items-center gap-3 justify-center px-4 py-3 rounded-xl
              bg-card border border-border shadow-sm
              hover:shadow-card-hover hover:border-accent/30 transition-all duration-200 group"
          >
            <div className={`p-2 rounded-lg bg-accent/10 ${item.color} group-hover:scale-110 transition-transform duration-200`}>
              <item.icon className="h-4 w-4" />
            </div>
            <span className="text-sm font-semibold text-foreground">{item.label}</span>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default TrustStrip;
