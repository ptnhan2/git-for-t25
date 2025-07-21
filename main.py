from markdowns.save_markdown import create_markdowns_directory
from markdowns.save_markdown import delete_markdowns_directory
from markdowns.chunking.save_chunks_to_md import save_chunks_markdowns
def main():
	# create_markdowns_directory()
	# delete_markdowns_directory()

	save_chunks_markdowns()

if __name__ == "__main__":
    main()