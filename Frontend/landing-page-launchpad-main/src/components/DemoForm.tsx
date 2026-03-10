import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";

const storeTypes = ["Kirana Store", "General Store", "Medical Store", "Hardware Store", "Margin Business"];

const DemoForm = ({ variant = "default" }: { variant?: "default" | "compact" }) => {
  const [form, setForm] = useState({ name: "", mobile: "", storeType: "", city: "" });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!form.name || !form.mobile || !form.storeType || !form.city) {
      toast.error("Please fill all fields");
      return;
    }

    try {
      setLoading(true);

      const response = await fetch("http://127.0.0.1:8000/book-demo/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: form.name,
          contact_number: form.mobile,   
          store_type: form.storeType,    
          city: form.city,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        toast.success("Demo request submitted! We'll contact you soon.");
        setForm({ name: "", mobile: "", storeType: "", city: "" });
        window.location.href = "/";
      } else {
        toast.error(data.error || "Something went wrong");
      }
    } catch (error) {
      toast.error("Server error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <Input
        placeholder="Your Name"
        value={form.name}
        onChange={(e) => setForm({ ...form, name: e.target.value })}
        className="bg-card border-border text-black placeholder-black/70"
      />
      <Input
        placeholder="Mobile Number"
        value={form.mobile}
        onChange={(e) => setForm({ ...form, mobile: e.target.value })}
        className="bg-card border-border text-black placeholder-black/70"
      />
      <select
        value={form.storeType}
        onChange={(e) => setForm({ ...form, storeType: e.target.value })}
        className="w-full h-10 rounded-md border border-border bg-card px-3 text-sm text-foreground text-black placeholder-black/70"
      >
        <option value="">Select Store Type</option>
        {storeTypes.map((s) => (
          <option key={s} value={s}>{s}</option>
        ))}
      </select>
      <Input
        placeholder="City"
        value={form.city}
        onChange={(e) => setForm({ ...form, city: e.target.value })}
        className="bg-card border-border text-black placeholder-black/70"
      />
      <Button
        type="submit"
        disabled={loading}
        className="w-full bg-gold-gradient text-accent-foreground font-semibold hover:opacity-90"
        // <-- redirect to home
      >
        {loading ? "Submitting..." : "Book Free Demo"}
      </Button>
    </form>
  );
};

export default DemoForm;