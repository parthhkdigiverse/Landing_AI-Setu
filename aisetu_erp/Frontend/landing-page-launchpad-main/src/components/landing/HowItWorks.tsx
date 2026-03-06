import { motion } from "framer-motion";
import { CalendarCheck, Settings, Rocket } from "lucide-react";

const steps = [
  { icon: CalendarCheck, num: "01", title: "Book Demo", desc: "Schedule a free demo with our team" },
  { icon: Settings, num: "02", title: "Setup & Training", desc: "We set up everything & train your staff" },
  { icon: Rocket, num: "03", title: "Start Smart Billing", desc: "Go live with AI-powered billing" },
];

const HowItWorks = () => (
  <section className="py-16 lg:py-24 bg-background">
    <div className="container">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center mb-12"
      >
        <span className="text-accent font-semibold text-sm uppercase tracking-wider">Simple Process</span>
        <h2 className="text-3xl lg:text-4xl font-bold mt-2 text-foreground">How It Works</h2>
      </motion.div>
      <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
        {steps.map((s, i) => (
          <motion.div
            key={s.num}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.15 }}
            className="text-center relative"
          >
            <div className="w-16 h-16 rounded-2xl bg-gold-gradient flex items-center justify-center mx-auto mb-4">
              <s.icon className="h-7 w-7 text-accent-foreground" />
            </div>
            <span className="text-xs font-bold text-accent tracking-widest">{s.num}</span>
            <h3 className="font-heading font-bold text-xl text-foreground mt-1 mb-2">{s.title}</h3>
            <p className="text-sm text-muted-foreground">{s.desc}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default HowItWorks;
