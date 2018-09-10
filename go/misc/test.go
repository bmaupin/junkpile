package main

import (
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"

	"github.com/bmaupin/go-util/htmlutil"
	"golang.org/x/net/html"
)

func main() {
	sourcesToTest := []string{
		"test.go",
		"/tmp/thisshouldfail",
		"https://golang.org/doc/gopher/gophercolor16x16.png",
		"http://thisshouldfail",
	}

	for _, source := range sourcesToTest {
		valid := isFileSourceValid(source)
		if valid == false {
			fmt.Println(source)
		}
	}

	/*
		if err := ioutil.WriteFile("/tmp/tmp/tmp/tmp", []byte(""), 0644); err != nil {
			panic(fmt.Sprintf("Error writing file: %s", err))
		}
	*/

	/*
		    // import "github.com/satori/go.uuid"
			u := uuid.NewV4()
			fmt.Println(u)
	*/
}

func isFileSourceValid(source string) bool {
	u, err := url.Parse(source)
	if err != nil {
		return false
	}

	var r io.ReadCloser
	var resp *http.Response
	// If it's a URL
	if u.Scheme == "http" || u.Scheme == "https" {
		resp, err = http.Get(source)
		if err != nil {
			return false
		}
		r = resp.Body

		// Otherwise, assume it's a local file
	} else {
		r, err = os.Open(source)
	}
	if err != nil {
		return false
	}
	defer func() {
		if err := r.Close(); err != nil {
			panic(err)
		}
	}()

	return true
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
