package main

import (
	"errors"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"

	"github.com/bmaupin/go-util/htmlutil"
	"golang.org/x/net/html"
)

func main() {
	err := testErrorType()
	// fmt.Println(err == ErrRetrievingFile)
	// fmt.Println(err.(type) == FileRetrevalError)
	// fmt.Println((*err).Error() == FileRetrevalError)
	// fmt.Println(err.Error())

	if (err == err.(*FileRetrevalError2)) {
		fmt.Println("FileRetrevalError2")
	}

	// if nerr, ok := err.(*FileRetrevalError); ok {
	// 	fmt.Println(ok)
	// 	fmt.Println(nerr)
	// }

	// sourcesToTest := []string{
	// 	"test.go",
	// 	"/tmp/thisshouldfail",
	// 	"https://golang.org/doc/gopher/gophercolor16x16.png",
	// 	"http://thisshouldfail",
	// }

	// for _, source := range sourcesToTest {
	// 	valid := isFileSourceValid(source)
	// 	if valid == false {
	// 		fmt.Println(source)
	// 	}
	// }

	// testMapSearch()

	/*
		// See what error is returned by ioutil.WriteFile when directory doesn't exist
		if err := ioutil.WriteFile("/tmp/tmp/tmp/tmp", []byte(""), 0644); err != nil {
			panic(fmt.Sprintf("Error writing file: %s", err))
		}
	*/

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


var ErrRetrievingFile = errors.New("Error retrieving file from source")

type FileRetrevalError2 struct {
	file string
	err  error
}
func (e *FileRetrevalError2) Error() string {
	return fmt.Sprintf("Error retrieving %q from source: %+v", e.file, e.err)
}

type FileRetrevalError struct {
	file string
	err  error
}
func (e *FileRetrevalError) Error() string {
	return fmt.Sprintf("Error retrieving %q from source: %+v", e.file, e.err)
}

func testErrorType() error {
	mediaSource := "/tmp/thisshouldfail"

	_, err := os.Open(mediaSource)
	if err != nil {
		// return ErrRetrievingFile
		// return &FileRetrevalError{file: mediaSource, err: err}
		return &FileRetrevalError2{file: mediaSource, err: err}
	}

	return nil
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

var testmap = map[string]string{
	"1": "one",
	"2": "two",
	"3": "three",
	"4": "four",
}

func testMapSearch() {
	ok := true
	var i int
	for i = 1; ok; i++ {
		fmt.Println(i)
		_, ok = testmap[string(i)]
	}

	fmt.Println(i)
}
