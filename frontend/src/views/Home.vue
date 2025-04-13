<template>
  <LoadingSpinner v-if="isLoading" />
  <div v-else class="home-container">
    <p v-if="error">{{ error }}</p>
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
                id="gas"
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
            <th>Electricity</th>
            <th>Electricity Price</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <input
                id="t1"
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
                id="t2"
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
                id="coldKitchen"
                type="number"
                placeholder="Cold. Kitchen"
                v-model="waterInput.kitchen.cold"
              />
            </td>
            <td>
              <input
                id="coldBathroom"
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
                id="hotKitchen"
                type="number"
                placeholder="Hot. Kitchen"
                v-model="waterInput.kitchen.hot"
              />
            </td>
            <td>
              <input
                id="hotBathroom"
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
      <button @click="sendData">Submit</button>
    </div>
    <div v-if="showResultBlock" class="home-container-result-block">
      <div class="show-result-button-block">
        <button
          @click="closeResultBlock"
          class="close-show-result-block-button"
        >
          X
        </button>
      </div>
      <div v-if="objectDetails" style="display: flex">
        <table>
          <thead>
            <tr>
              <th></th>
              <th>Category</th>
              <th>New input</th>
              <th>Previous input</th>
              <th>Consumption</th>
              <th>Price/unit</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Gas</td>
              <td></td>
              <td>{{ objectDetails.utilities.gas.current }}</td>
              <td>{{ objectDetails.utilities.gas.previous }}</td>
              <td>{{ objectDetails.utilities.gas.consumption }}</td>
              <td>{{ objectDetails.prices.gas }}</td>
              <td>{{ objectDetails.cost.gas }}</td>
            </tr>
            <tr>
              <td>Water</td>
              <td>Cold kitchen</td>
              <td>{{ objectDetails.utilities.water.cold.kitchen.current }}</td>
              <td>{{ objectDetails.utilities.water.cold.kitchen.previous }}</td>
              <td>
                {{ objectDetails.utilities.water.cold.kitchen.consumption }}
              </td>
              <td>{{ objectDetails.prices.water.cold }}</td>
              <td>{{ objectDetails.cost.water.kitchen_cold }}</td>
            </tr>
            <tr>
              <td></td>
              <td>Cold bathroom</td>
              <td>{{ objectDetails.utilities.water.cold.bathroom.current }}</td>
              <td>
                {{ objectDetails.utilities.water.cold.bathroom.previous }}
              </td>
              <td>
                {{ objectDetails.utilities.water.cold.bathroom.consumption }}
              </td>
              <td>{{ objectDetails.prices.water.cold }}</td>
              <td>{{ objectDetails.cost.water.bathroom_cold }}</td>
            </tr>
            <tr>
              <td></td>
              <td>Hot kitchen</td>
              <td>{{ objectDetails.utilities.water.hot.kitchen.current }}</td>
              <td>
                {{ objectDetails.utilities.water.hot.kitchen.previous }}
              </td>
              <td>
                {{ objectDetails.utilities.water.hot.kitchen.consumption }}
              </td>
              <td>{{ objectDetails.prices.water.hot }}</td>
              <td>{{ objectDetails.cost.water.kitchen_hot }}</td>
            </tr>
            <tr>
              <td></td>
              <td>Hot bathroom</td>
              <td>{{ objectDetails.utilities.water.hot.bathroom.current }}</td>
              <td>
                {{ objectDetails.utilities.water.hot.bathroom.previous }}
              </td>
              <td>
                {{ objectDetails.utilities.water.hot.bathroom.consumption }}
              </td>
              <td>{{ objectDetails.prices.water.hot }}</td>
              <td>{{ objectDetails.cost.water.bathroom_hot }}</td>
            </tr>
            <tr>
              <td>Electricity</td>
              <td>T1</td>
              <td>{{ objectDetails.utilities.electricity.t1.current }}</td>
              <td>{{ objectDetails.utilities.electricity.t1.previous }}</td>
              <td>
                {{ objectDetails.utilities.electricity.t1.consumption }}
              </td>
              <td>{{ objectDetails.prices.electricity.t1 }}</td>
              <td>{{ objectDetails.cost.electricity.t1 }}</td>
            </tr>
            <tr>
              <td></td>
              <td>T2</td>
              <td>{{ objectDetails.utilities.electricity.t2.current }}</td>
              <td>{{ objectDetails.utilities.electricity.t2.previous }}</td>
              <td>
                {{ objectDetails.utilities.electricity.t2.consumption }}
              </td>
              <td>{{ objectDetails.prices.electricity.t2 }}</td>
              <td>{{ objectDetails.cost.electricity.t2 }}</td>
            </tr>
            <tr>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
              <td>Total cost:</td>
              <td>{{ objectDetails.cost.total_cost }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div></div>
    </div>
    <div class="home-container-history-block">
      <div v-for="object in utilitiesList" :key="object" class="history-object">
        <button @click="getObjectResult(object.date)">
          {{ object.formattedDate }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import { dateToString, sortByDate } from "@/services/main";
import { useAuthStore } from "@/stores/auth";
import { fetchAuthSession } from "aws-amplify/auth";
import { ref, onMounted, watch } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "Home",
  components: {
    LoadingSpinner,
  },

  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    const COUNT_URL =
      "https://rtem6et0wh.execute-api.eu-central-1.amazonaws.com/dev/count";

    const error = ref(null);

    const utilitiesList = ref(null);

    // Input
    const gasInput = ref(null);
    const waterInput = ref({
      kitchen: { cold: null, hot: null },
      bathroom: { cold: null, hot: null },
    });
    const electricityInput = ref(null);
    const t1electricityInput = ref(null);
    const t2electricityInput = ref(null);

    // Prices
    const gasPrice = ref(null);
    const gasDistribution = ref(null);
    const waterColdPrice = ref(null);
    const waterHotPrice = ref(null);
    const electricityPrice = ref(null);
    const t1electricityPrice = ref(null);
    const t2electricityPrice = ref(null);

    const objectDetails = ref(null);
    const showResultBlock = ref(false);
    const isLoading = ref(true);

    onMounted(async () => {
      try {
        await getCurrentSession();
        await getData();
      } catch (err) {
        console.log("Error in mounted:", err);
      } finally {
        isLoading.value = false;
      }
    });

    const getCurrentSession = async () => {
      try {
        const session = await fetchAuthSession();

        if (session) {
          await setUserSession(session);
        }
      } catch (err) {
        redirectToSignIn();
        console.log("No user on mounted in Home.");
      }
    };
    const setUserSession = async (session) => {
      authStore.setUser({
        user: {
          username: session.userSub,
          email: session.tokens.signInDetails?.loginId,
        },
        isLoggedIn: true,
        authToken: session.tokens.idToken.toString(),
      });
    };
    const redirectToSignIn = () => {
      router.push("/signin");
    };
    const getData = async () => {
      try {
        const resp = await fetch(COUNT_URL, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authStore.authToken}`,
          },
        });
        const data = await resp.json();
        if (resp.status !== 200) {
          console.log("Server side error: ", data.error);
          utilitiesList.value = [];
          error.value = "Bad request error.";
        } else {
          utilitiesList.value = sortByDate(data.utilities_list, "desc");
        }
      } catch (error) {
        console.log("GET request error: ", error);
      }
    };
    const sendData = async () => {
      const payload = {
        date: dateToString(),
        utilities: {
          gas: gasInput.value,
          electricity: {
            t1: t1electricityInput.value,
            t2: t2electricityInput.value,
          },
          water: {
            cold: {
              kitchen: waterInput.value.kitchen.cold,
              bathroom: waterInput.value.bathroom.cold,
            },
            hot: {
              kitchen: waterInput.value.kitchen.hot,
              bathroom: waterInput.value.bathroom.hot,
            },
          },
        },
        prices: {
          gas: gasPrice.value,
          gas_distribution: gasDistribution.value,
          electricity: {
            t1: t1electricityPrice.value,
            t2: t2electricityPrice.value,
          },
          water: {
            cold: waterColdPrice.value,
            hot: waterHotPrice.value,
          },
        },
      };
      console.log("Submitted data:", payload);
      try {
        const response = await fetch(COUNT_URL, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authStore.authToken}`,
          },
          body: JSON.stringify({
            body: { payload },
          }),
        });
        const data = await response.json();
        if (response.status !== 200) {
          console.log("Server side error: ", data.error);
          error.value = "Bad request error.";
        } else {
          console.log("POST -> Response from server:", data);
          showResultBlock.value = false;
          await getData();
          // remove input values
          cleanInputs();
        }
      } catch (error) {
        console.log("POST request error: ", error);
      }
    };
    const cleanInputs = () => {
      gasInput.value = null;
      waterInput.value = {
        kitchen: { cold: null, hot: null },
        bathroom: { cold: null, hot: null },
      };
      t1electricityInput.value = null;
      t2electricityInput.value = null;
      electricityInput.value = null;
    };

    const getObjectResult = (date) => {
      objectDetails.value = utilitiesList.value.find(
        (object) => object.date === date
      );
      console.log("Object details:", objectDetails.value);
      showResultBlock.value = true;
    };
    const closeResultBlock = () => {
      showResultBlock.value = false;
    };

    // Observes for price changes and put ones into input fields.
    watch(utilitiesList, (newValue) => {
      if (newValue.length !== 0) {
        const sortedData = sortByDate(newValue, "desc");
        const lastObjByDate = sortedData[0];
        gasPrice.value = lastObjByDate.prices.gas;
        gasDistribution.value = lastObjByDate.prices.gas_distribution;
        t1electricityPrice.value = lastObjByDate.prices.electricity.t1;
        t2electricityPrice.value = lastObjByDate.prices.electricity.t2;
        waterColdPrice.value = lastObjByDate.prices.water.cold;
        waterHotPrice.value = lastObjByDate.prices.water.hot;
      }
    });

    return {
      // API request
      sendData,
      // Inputs
      waterInput,
      gasInput,
      t1electricityInput,
      t2electricityInput,
      electricityInput,
      // Prices
      gasPrice,
      gasDistribution,
      waterColdPrice,
      waterHotPrice,
      electricityPrice,
      t1electricityPrice,
      t2electricityPrice,
      // Data
      objectDetails,
      utilitiesList,
      getObjectResult,
      // Functions
      closeResultBlock,
      // Other
      isLoading,
      showResultBlock,
      error,
    };
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
  background-color: #1f2937; /* Dark Theme: Dark slate gray background */
  color: #d1d5db; /* Dark Theme: Light gray default text color */
}

/* Style the input block containing all tables */
.home-container-input-block {
  display: flex;
  gap: 20px;
  background-color: #374151; /* Dark Theme: Medium-dark gray */
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3); /* Dark Theme: Adjusted shadow for dark bg */
}
.home-container-result-block {
  display: flex;
  flex-direction: column;
  gap: 20px;
  background-color: #374151; /* Dark Theme: Medium-dark gray */
  padding: 20px;
  border-radius: 8px;
  margin-top: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3); /* Dark Theme: Adjusted shadow for dark bg */
  position: relative;
}
/* Container for history objects */
.home-container-history-block {
  display: flex;
  flex-wrap: wrap; /* ADDED: Allows items to wrap onto multiple lines */
  justify-content: flex-start; /* CHANGED: Aligns items to the start of each line */
  gap: 20px; /* Keeps consistent spacing between items, both horizontally and vertically */
  padding: 20px;
  border-radius: 8px;
  margin: 0 10px; /* Existing margin */
  margin-top: 1.5rem; /* Existing margin */
  /* You might want to ensure this container has a background matching the theme */
  /* e.g., background-color: #374151; */
}

/* Individual history object styling (remains the same) */
.history-object {
  background-color: #4b5563; /* Dark Theme: Slightly lighter gray for history objects */
  padding: 10px;
  border-radius: 8px;
  color: #f9fafb; /* Dark Theme: Very light gray/white text for contrast */
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3); /* Dark Theme: Adjusted shadow */
  /* Optional: You might want to add a min-width or width to history objects */
  /* E.g., min-width: 100px; */
}

/* Table styling */
table {
  width: 100%;
  max-width: 600px;
  border-collapse: collapse;
  background-color: #2d3748; /* Dark Theme: Slightly darker gray for table */
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3); /* Dark Theme: Adjusted shadow */
  overflow: hidden;
}

/* Table header styling */
thead th {
  background-color: #4b5563; /* Dark Theme: Slightly lighter gray for headers */
  color: #f9fafb; /* Dark Theme: Very light gray/white text for contrast */
  padding: 10px;
  text-align: left;
  font-weight: 600;
}

/* Table body styling */
tbody td {
  padding: 10px;
  border-bottom: 1px solid #4b5563; /* Dark Theme: Medium gray border */
  color: #d1d5db; /* Dark Theme: Light gray text */
}

/* Input styling */
input[type="number"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #4b5563; /* Dark Theme: Medium gray border */
  border-radius: 4px;
  font-size: 14px;
  background-color: #1f2937; /* Dark Theme: Dark background for input */
  color: #e5e7eb; /* Dark Theme: Lighter text for input */
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
  border-color: #60a5fa; /* Soft blue for focus (often okay on dark) */
  outline: none;
  box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.3); /* Dark Theme: Slightly more opaque focus ring */
}

/* Placeholder text styling */
input::placeholder {
  color: #6b7280; /* Dark Theme: Dimmer gray for placeholder */
  font-style: italic;
}

/* Hover effect for table rows */
tbody tr:hover {
  background-color: #212831; /* Dark Theme: Slightly lighter gray for hover */
}

/* Button styling */
.home-container-input-block button {
  background-color: #3b82f6; /* Clean blue (usually contrasts well) */
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

.show-result-button-block {
  position: absolute; /* Takes the button out of normal document flow */
  top: 0;
  right: 0;
  padding: 5px; /* Optional: adds some space around the button */
}

.close-show-result-block-button {
  background: none;
  border: 1px solid #4b5563; /* Dark Theme: Medium gray border */
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  padding: 5px 10px; /* Adjust padding as needed */
  /* Optional styling to make the button more visible */
  color: #ffff;
  font-weight: bold;
}

.close-show-result-block-button:hover {
  color: #ffff; /* Optional hover effect */
  background-color: #4b5563; /* Dark Theme: Medium gray background */
  border: 1px solid #f7537c; /* Clean blue border */
}

/* Responsive adjustments (no color changes needed here) */
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
