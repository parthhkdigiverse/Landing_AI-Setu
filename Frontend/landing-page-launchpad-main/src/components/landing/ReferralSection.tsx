import { motion } from "framer-motion";
import { Gift, RefreshCw, Infinity, UserPlus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

const perks = [
  { icon: Gift, title: "₹2,000", desc: "Per Successful Sale" },
  { icon: RefreshCw, title: "₹1,000", desc: "Renewal Incentive" },
  { icon: UserPlus, title: "₹1,000", desc: "For Every Successful Referral Purchase" },
  { icon: Infinity, title: "Unlimited", desc: "Referrals Allowed" },
];

const ReferralSection = () => {
  const navigate = useNavigate();

  return (
    <section className="py-16 lg:py-24 bg-hero text-primary-foreground">
      <div className="container">

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <span className="text-accent font-semibold text-sm uppercase tracking-wider">
            Referral Program
          </span>

          <h2 className="text-3xl lg:text-4xl font-bold mt-2">
            Earn With AI-Setu ERP
          </h2>
        </motion.div>

        <div className="grid md:grid-cols-4 gap-8 max-w-4xl mx-auto mb-10">
          {perks.map((p, i) => (
            <motion.div
              key={p.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="text-center"
            >
              <div className="w-14 h-14 rounded-xl bg-accent/20 flex items-center justify-center mx-auto mb-3">
                <p.icon className="h-7 w-7 text-accent" />
              </div>

              <h3 className="text-2xl font-bold text-gradient-gold">
                {p.title}
              </h3>

              <p className="text-primary-foreground/70 text-sm mt-1">
                {p.desc}
              </p>
            </motion.div>
          ))}
        </div>
        <div className="text-center">
          <Button
            onClick={() => navigate("/referral")}
            className="bg-gold-gradient text-accent-foreground font-semibold hover:opacity-90 px-8"
          >
            Join Referral Program
          </Button>
        </div>
      </div>
    </section>
  );
};

export default ReferralSection;