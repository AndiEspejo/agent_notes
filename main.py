import os
import argparse
from api.server import start_server

def main():
    parser = argparse.ArgumentParser(description="Local Study Agent")
    parser.add_argument("--docs_dir", type=str, help="Directory for documents")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    args = parser.parse_args()
    
    # Override documents directory if provided
    if args.docs_dir:
        from config.settings import settings
        settings.documents_dir = os.path.abspath(args.docs_dir)
    
    if args.cli:
        # Run in CLI mode
        from core.agent import StudyAgent
        
        # Initialize and start the agent
        agent = StudyAgent()
        agent.start()
        
        print("Study Agent is ready! Type 'exit' to quit.")
        
        try:
            while True:
                user_input = input("\nYou: ")
                
                if user_input.lower() in ("exit", "quit"):
                    break
                    
                response = agent.chat(user_input)
                print(f"\nAgent: {response}")
                
        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            agent.stop()
    else:
        # Run the web server
        start_server()

if __name__ == "__main__":
    main() 