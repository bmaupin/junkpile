// Misc functions

package functions

import (
	"archive/zip"
	"io"
	"os"
	"path/filepath"
)

func CopyFile(sourceFilePath string, destFilePath string) error {
	r, err := os.Open(sourceFilePath)
	if err != nil {
		return err
	}
	defer func() {
		err = r.Close()
	}()

	w, err := os.Create(destFilePath)
	if err != nil {
		return err
	}
	defer func() {
		err = w.Close()
	}()

	_, err = io.Copy(w, r)
	if err != nil {
		return err
	}

	return err
}

func ZipFile(sourceFilePath string, destFilePath string) error {
	r, err := os.Open(sourceFilePath)
	if err != nil {
		return err
	}
	defer func() {
		err = r.Close()
	}()

	f, err := os.Create(destFilePath)
	if err != nil {
		return err
	}
	defer func() {
		err = f.Close()
	}()

	z := zip.NewWriter(f)
	defer func() {
		err = z.Close()
	}()

	w, err := z.Create(sourceFilePath)
	if err != nil {
		return err
	}

	_, err = io.Copy(w, r)
	if err != nil {
		return err
	}

	return err
}

func ZipFolder(sourceFolderPath string, destFilePath string) error {
	f, err := os.Create(destFilePath)
	if err != nil {
		return err
	}
	defer func() {
		err = f.Close()
	}()

	z := zip.NewWriter(f)
	defer func() {
		err = z.Close()
	}()

	var addFileToZip = func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		// Get the path of the file relative to the folder we're zipping
		relativePath, err := filepath.Rel(sourceFolderPath, path)
		if err != nil {
			return err
		}

		// Only include regular files, not directories
		if !info.Mode().IsRegular() {
			return nil
		}

		r, err := os.Open(path)
		if err != nil {
			return err
		}
		defer func() {
			err = r.Close()
		}()

		w, err := z.Create(relativePath)
		if err != nil {
			return err
		}

		_, err = io.Copy(w, r)
		if err != nil {
			return err
		}

		return err
	}

	err = filepath.Walk(sourceFolderPath, addFileToZip)
	if err != nil {
		return err
	}

	return err
}
