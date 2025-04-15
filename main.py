import threading

from utils import crime_reporting_mode, display_serp_results, extract_crime_features, deep_learning_mode, extract_deep_learning_subheadings, general_search_mode, get_features_keywords, perform_search, ThreadPoolExecutor, API_KEY, SEARCH_ENGINE_ID


# MAIN PROGRAM (USER MENU)
# =========================
def main():
    while True:
        print("\nSelect mode:")
        print("1: General Search")
        print("2: Crime Reporting Papers Analysis")
        print("3: Deep Learning Journal Papers Analysis")
        print("4: Exit")
        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            t = threading.Thread(target=general_search_mode)
            t.start()
            t.join()
        elif choice == "2":
            t = threading.Thread(target=crime_reporting_mode)
            t.start()
            t.join()
        elif choice == "3":
            t = threading.Thread(target=deep_learning_mode)
            t.start()
            t.join()
        elif choice == "4":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()