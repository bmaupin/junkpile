package main

import (
	"fmt"
	"io/ioutil"

	"github.com/bmaupin/go-util/htmlutil"
	"golang.org/x/net/html"
)

func main() {
	if err := ioutil.WriteFile("/tmp/tmp/tmp/tmp", []byte(""), 0644); err != nil {
		panic(fmt.Sprintf("Error writing file: %s", err))
	}

	/*
		    // import "github.com/satori/go.uuid"
			u := uuid.NewV4()
			fmt.Println(u)
	*/
}

func debugNode(node *html.Node) {
	fmt.Printf("type: %s\n", node.Type)
	if node.Type == html.CommentNode {
		fmt.Println("type: CommentNode")
	} else if node.Type == html.DoctypeNode {
		fmt.Println("type: DoctypeNode")
	} else if node.Type == html.DocumentNode {
		fmt.Println("type: DocumentNode")
	} else if node.Type == html.ElementNode {
		fmt.Println("type: ElementNode")
	} else if node.Type == html.ErrorNode {
		fmt.Println("type: ErrorNode")
	} else if node.Type == html.TextNode {
		fmt.Println("type: TextNode")
	}

	fmt.Printf("data: %s\n", node.Data)
	fmt.Printf("attr: %s\n", node.Attr)
	fmt.Println(htmlutil.HtmlNodeToString(node))
}
