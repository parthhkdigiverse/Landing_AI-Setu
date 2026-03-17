import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";
import { useNavigate } from "react-router-dom";
import { API_BASE_URL } from "@/services/api";

const DemoForm = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", mobile: "", storeType: "", city: "" });
  const [loading, setLoading] = useState(false);
  
  // State for dynamic store types
  const [storeTypes, setStoreTypes] = useState<{id: number, name: string}[]>([]);

  useEffect(() => {
    const fetchTypes = async () => {
      try {
        // Ensure this URL exactly matches your urls.py path
        const response = await fetch(`${API_BASE_URL}/api/all-storetype/`);
        const data = await response.json();
        console.log("Data from Admin:", data); // Check F12 console
        setStoreTypes(data);
      } catch (error) {
        console.error("Could not load store types from API", error);
      }
    };

    fetchTypes();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.name || !form.mobile || !form.storeType || !form.city) {
      toast.error("Please fill all fields");
      return;
    }

    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/book-demo/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: form.name,
          contact_number: form.mobile,
          store_type: form.storeType,
          city: form.city,
        }),
      });

      if (response.ok) {
        navigate("/demo-success"); 
      } else {
        toast.error("Submission failed");
      }
    } catch (error) {
      toast.error("Server error");
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
      
      {/* Dropdown now pulls from 'storeTypes' state */}
      <select
        value={form.storeType}
        onChange={(e) => setForm({ ...form, storeType: e.target.value })}
        className="w-full h-10 rounded-md border border-border bg-card px-3 text-sm text-black"
      >
        <option value="">Select Store Type</option>
        {storeTypes.length > 0 ? (
          storeTypes.map((s) => (
            <option key={s.id} value={s.name}>
              {s.name}
            </option>
          ))
        ) : (
          <option disabled>Loading types...</option>
        )}
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
        className="w-full bg-gold-gradient text-accent-foreground font-semibold"
      >
        {loading ? "Submitting..." : "Book Free Demo"}
      </Button>
    </form>
  );
};

export default DemoForm;