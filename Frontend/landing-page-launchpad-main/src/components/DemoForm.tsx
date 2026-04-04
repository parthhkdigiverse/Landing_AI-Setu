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
        const response = await fetch(`${API_BASE_URL}/api/all-storetype/`);
        const contentType = response.headers.get("content-type");
        if (!response.ok || !contentType || !contentType.includes("application/json")) {
          throw new Error(`Server returned ${response.status}: ${response.statusText}`);
        }
        const data = await response.json();
        setStoreTypes(data);
      } catch (error) {
        console.error("Could not load store types from API", error);
      }
    };

    fetchTypes();
  }, []);

  // ✅ Listen for live preview updates from django-admin to update the dropdown dynamically
  useEffect(() => {
    const handler = (event: MessageEvent) => {
      if (event.data?.source === "django-admin" && event.data?.model === "AllStoreType") {
        const payload = event.data.payload;
        setStoreTypes((prev) => {
          // If editing an existing one, map and update name; else append it.
          // Since we don't have the real ID from payload immediately, we replace if the name exists.
          const existing = prev.find((st) => st.name === payload.name);
          if (existing) {
            return prev.map((st) => (st.name === payload.name ? { ...st, name: payload.name } : st));
          }
          // If it's totally new or name changed, append to dropdown.
          return [...prev, { id: 99999 + prev.length, name: payload.name }];
        });
        // ✅ Auto-select it so the admin sees it clearly in the preview without clicking
        setForm((f) => ({ ...f, storeType: payload.name }));
      }
    };
    window.addEventListener("message", handler);
    return () => window.removeEventListener("message", handler);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.name || !form.mobile || !form.storeType || !form.city) {
      toast.error("Please fill all fields");
      return;
    }

    if (form.mobile.length !== 10) {
      toast.error("Please enter a valid 10-digit mobile number");
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
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
           const data = await response.json();
           toast.error(data.error || "Submission failed");
        } else {
           toast.error("Submission failed: Server error");
        }
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
        type="tel"
        placeholder="Mobile Number"
        value={form.mobile}
        onChange={(e) => {
          const val = e.target.value;
          const numericVal = val.replace(/\D/g, "");
          if (val !== numericVal) {
            toast.error("Please enter numbers only");
          }
          if (numericVal.length <= 10) {
            setForm({ ...form, mobile: numericVal });
          }
        }}
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