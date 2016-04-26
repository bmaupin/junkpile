package main

import (
	"fmt"
	"io/ioutil"
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
