<template>
  <div class="home-container">
    <div class="home-container-input-block">
      <table>
        <thead>
          <tr>
            <th>Gas</th>
            <th>Gas Price</th>
            <th>Gas Distribution</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <input
                type="number"
                placeholder="Gas numbers"
                v-model="gasInput"
              />
            </td>
            <td>
              <input type="number" placeholder="$/m3" v-model="gasPrice" />
            </td>
            <td>
              <input type="number" placeholder="$" v-model="gasDistribution" />
            </td>
          </tr>
        </tbody>
      </table>
      <table>
        <thead>
          <tr>
            <th>Heat</th>
            <th>Heat Price</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <input
                type="number"
                placeholder="Heat numbers"
                v-model="heatInput"
              />
            </td>
            <td>
              <input type="number" placeholder="$/m3" v-model="heatPrice" />
            </td>
          </tr>
        </tbody>
      </table>
      <table>
        <thead>
          <tr>
            <th>Electricity</th>
            <th>Electricity Price</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <input
                type="number"
                placeholder="T1"
                v-model="t1electricityInput"
              />
            </td>
            <td>
              <input
                type="number"
                placeholder="$/kw"
                v-model="t1electricityPrice"
              />
            </td>
          </tr>
          <tr>
            <td>
              <input
                type="number"
                placeholder="T2"
                v-model="t2electricityInput"
              />
            </td>
            <td>
              <input
                type="number"
                placeholder="$/kw"
                v-model="t2electricityPrice"
              />
            </td>
          </tr>
        </tbody>
      </table>
      <table>
        <thead>
          <tr>
            <th>Kitchen</th>
            <th>Bathroom</th>
            <th>Price</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <input
                type="number"
                placeholder="Cold. Kitchen"
                v-model="waterInput.kitchen.cold"
              />
            </td>
            <td>
              <input
                type="number"
                placeholder="Cold. Bathroom"
                v-model="waterInput.bathroom.cold"
              />
            </td>
            <td>
              <input
                type="number"
                placeholder="Price, m3"
                v-model="waterColdPrice"
              />
            </td>
          </tr>
          <tr>
            <td>
              <input
                type="number"
                placeholder="Hot. Kitchen"
                v-model="waterInput.kitchen.hot"
              />
            </td>
            <td>
              <input
                type="number"
                placeholder="Hot. Bathroom"
                v-model="waterInput.bathroom.hot"
              />
            </td>
            <td>
              <input
                type="number"
                placeholder="Price, m3"
                v-model="waterHotPrice"
              />
            </td>
          </tr>
        </tbody>
      </table>
      <button @click="sendInputData">Submit</button>
    </div>
    <button @click="getReq">Get</button>
  </div>
</template>

<script>
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import { fetchAuthSession } from "aws-amplify/auth";
import { ref } from "vue";

export default {
  name: "Home",

  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    const COUNT_URL =
      "https://a8lx65txd8.execute-api.eu-central-1.amazonaws.com/dev/count";

    const resp = null;

    const gasInput = ref(null);
    const gasPrice = ref(null);
    const gasDistribution = ref(null);
    const waterInput = ref({
      kitchen: { cold: null, hot: null },
      bathroom: { cold: null, hot: null },
    });
    const waterColdPrice = ref(null);
    const waterHotPrice = ref(null);
    const heatInput = ref(null);
    const heatPrice = ref(null);
    const electricityInput = ref(null);
    const electricityPrice = ref(null);
    const t1electricityInput = ref(null);
    const t1electricityPrice = ref(null);
    const t2electricityInput = ref(null);
    const t2electricityPrice = ref(null);

    return {
      authStore,
      router,
      COUNT_URL,
      waterInput,
      gasInput,
      gasPrice,
      gasDistribution,
      waterColdPrice,
      waterHotPrice,
      heatInput,
      heatPrice,
      electricityInput,
      electricityPrice,
      t1electricityInput,
      t1electricityPrice,
      t2electricityInput,
      t2electricityPrice,
      resp,
    };
  },
  //TODO: to think abot getCurrentUser and fetchAuthSession
  async mounted() {
    try {
      const session = await fetchAuthSession();

      if (session) {
        this.authStore.setUser({
          user: {
            username: session.userSub,
            email: session.tokens.signInDetails?.loginId,
          },
          isLoggedIn: true,
          authToken: session.tokens.idToken.toString(),
        });
      }
    } catch (err) {
      this.router.push("/signin");
      console.log("No user on mounted in Home.");
    }
  },
  methods: {
    async sendInputData() {
      // This method will handle the submission of input data
      const inputData = {
        gasInput: this.gasInput,
        gasPrice: this.gasPrice,
        gasDistribution: this.gasDistribution,
        waterInput: this.waterInput,
        waterColdPrice: this.waterColdPrice,
        waterHotPrice: this.waterHotPrice,
        heatInput: this.heatInput,
        heatPrice: this.heatPrice,
        electricityInput: this.electricityInput,
        electricityPrice: this.electricityPrice,
        t1electricityInput: this.t1electricityInput,
        t1electricityPrice: this.t1electricityPrice,
        t2electricityInput: this.t2electricityInput,
        t2electricityPrice: this.t2electricityPrice,
      };
      console.log("Submitted data:", inputData);
      const response = await fetch(this.COUNT_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${this.authStore.authToken}`,
        },
        body: JSON.stringify(inputData),
      });
      const data = await response.json();
      this.resp = data;
      console.log("Response from server:", data);
    },
    async getReq() {
      const resp = await fetch(this.COUNT_URL, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${this.authStore.authToken}`,
        },
      });
      const data = await resp.json();
      this.resp = JSON.parse(data.body);
      console.log("Response from server:", this.resp);
    },
  },
};
</script>

<style>
/* Style the main container */
.home-container {
  display: flex;
  align-items: center;
  flex-direction: column;
  padding: 20px;
  background-color: #f9fafb; /* Very light gray for a clean background */
}

/* Style the input block containing all tables */
.home-container-input-block {
  display: flex;
  flex-direction: column;
  gap: 20px;
  background-color: #ffffff; /* Pure white for a crisp look */
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
}

/* Table styling */
table {
  width: 100%;
  max-width: 600px;
  border-collapse: collapse;
  background-color: #ffffff; /* White for tables */
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* Table header styling */
thead th {
  background-color: #e5e7eb; /* Light gray for headers */
  color: #374151; /* Dark gray text for contrast */
  padding: 10px;
  text-align: left;
  font-weight: 600;
}

/* Table body styling */
tbody td {
  padding: 10px;
  border-bottom: 1px solid #e5e7eb; /* Light gray border */
  color: #4b5563; /* Medium gray text */
}

/* Input styling */
input[type="number"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #d1d5db; /* Light gray border */
  border-radius: 4px;
  font-size: 14px;
  background-color: #ffffff; /* White background */
  color: #374151; /* Dark gray text */
  transition: border-color 0.3s ease;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

/* Remove arrows specifically for Firefox */
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox fallback */
input[type="number"] {
  appearance: textfield;
  -moz-appearance: textfield;
}

input[type="number"]:focus {
  border-color: #60a5fa; /* Soft blue for focus */
  outline: none;
  box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.2); /* Subtle focus ring */
}

/* Placeholder text styling */
input::placeholder {
  color: #9ca3af; /* Light gray for placeholder */
  font-style: italic;
}

/* Hover effect for table rows */
tbody tr:hover {
  background-color: #f3f4f6; /* Very light gray for hover */
}

/* Button styling */
.home-container-input-block button {
  background-color: #3b82f6; /* Clean blue for buttons */
  color: #ffffff; /* White text */
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.home-container-input-block button:hover {
  background-color: #2563eb; /* Slightly darker blue on hover */
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .home-container-input-block {
    gap: 15px;
  }

  table {
    max-width: 100%;
  }

  input[type="number"] {
    font-size: 12px;
    padding: 6px;
  }
}
</style>
